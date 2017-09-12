import os
from flask import Flask
import pika
from configparser import ConfigParser
from flask import request
from flask import Response
import json

app = Flask(__name__)


def send_message_to_queue(message, source):
    try:
        config = ConfigParser()
        file = os.path.dirname(os.path.abspath(__file__)) + "/../common.cfg"
        config.read(file)
        server = config.get("broker", "server")
        queue_name = config.get("broker", "queue_name")
        queue_user = config.get("broker", "username")
        queue_password = config.get("broker", "password")
        credentials = pika.PlainCredentials(queue_user, queue_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=server, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        msg_js = json.dumps({"source": source, "data": json.loads(message.decode("utf-8"))})
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=msg_js)
    except Exception as e:
        print("Exception: ", e)


# this should be as simple as possible
@app.route('/facebook', methods=['GET', 'POST'])
def receive_message_facebook():
    print("GOT MESSAGE from facebook: ", request.data, request.args)
    if request.method == "POST":
        send_message_to_queue(request.data, "FACEBOOK")
    elif request.method == 'GET' and request.args.get('hub.verify_token') == "toto":
        return Response(request.args.get('hub.challenge'), status=200)
    return Response("OK", status=200)


if __name__ == "__main__":
    # neverdie loop to make sure we don't cut the connection with the channel
    while 1:
        try:
            app.run(host="0.0.0.0", debug=True, port=5013)
        except Exception as e:
            print("there was a call that we couldn't handle. The server will be relaunched. Exception: {0}".format(e))

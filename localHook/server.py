from flask import Flask
import os
from flask import Flask
import pika
from configparser import ConfigParser
import json
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)
chat_websocket = None


def send_message_to_queue(message, source):
    try:
        config = ConfigParser()
        file = os.path.dirname(os.path.abspath(__file__)) + "/../common.cfg"
        config.read(file)
        server = config.get("broker", "server")
        queue_name = config.get("broker", "queue_name")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=server))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        msg_js = json.dumps({"source": source, "data": message})
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=msg_js)
    except Exception as e:
        print("Exception: ", e)


@sockets.route('/')
def receive_socket(ws):
    global chat_websocket
    chat_websocket = ws
    while not ws.closed:
        message = chat_websocket.receive()
        print("message received: ", message)
        send_message_to_queue(message, "LOCAL")


@sockets.route('/echo')
def echo_socket(ws):
    global chat_websocket
    message = ws.receive()
    chat_websocket.send(message)
    print("message sent: ", message)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('0.0.0.0', 5044), app, handler_class=WebSocketHandler)
    server.serve_forever()

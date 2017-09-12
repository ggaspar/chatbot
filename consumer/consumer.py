import json
import time
from configparser import ConfigParser
import os
import pika
import facebook_connector


def message_handler(ch=None, method=None, properties=None, body=None, is_test=False):
    json_body = json.loads(body.decode("utf-8"))
    #handle message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run_consumer(credentials):
    tries = 1
    while 1:
        time.sleep(5)
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=server,credentials=credentials))
            channel = connection.channel()
            channel.queue_declare(queue=queue_name)
            break
        except Exception as e:
            tries += 1
            if tries > attempts_to_connect:
                raise Exception("FAILED to connect to server {0}. Exception {1}".format(server, e))

    channel.basic_consume(message_handler, queue=queue_name)
    channel.start_consuming()


if __name__ == "__main__":
    facebook_connector.Facebook.initial_setup()
    config = ConfigParser()
    file = os.path.dirname(os.path.abspath(__file__)) + "/../common.cfg"
    config.read(file)
    server = config.get("broker", "server")
    queue_name = config.get("broker", "queue_name")
    queue_user = config.get("broker", "username")
    queue_password = config.get("broker", "password")
    credentials = pika.PlainCredentials(queue_user, queue_password)
    attempts_to_connect = int(config.get("consumer", "attempts_to_connect"))
    while 1:
        try:
            run_consumer(credentials)
        except Exception as e:
            #hanndle error
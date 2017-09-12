import json
from configparser import ConfigParser
import os
import requests
import message_manager

#most of the functions could be refactor, to implement a proper sdk
class Facebook:
    def send_message(self, message):
        if message is None:
            return True
        if type(message) == str:
            return self.send_text(text=message)
        # res = self.initial_setup()
        elif message.content_type == message_manager.ContentType.URL:
            return self.send_url_button(message.text, message.urls_text, message.urls)
        elif message.content_type == message_manager.ContentType.BUTTON:
            return self.send_button(message.text, message.titles)
        elif message.content_type == message_manager.ContentType.TEXT:
            return self.send_text(text=message.text)
        elif message.content_type == message_manager.ContentType.FILE:
            return self.send_file(url=message.urls[0])
        elif message.content_type == message_manager.ContentType.QUICK_REPLY:
            return self.send_quick_replies(text=message.text,
                                           buttons_text=message.buttons_text,
                                           buttons_action=message.buttons_action)
        elif message.content_type == message_manager.ContentType.IMAGE:

            return self.send_image(image_url=message.text)
        else:
            return False

    def send_file(self, url):
        request = {
            "recipient": {"id": self.recipient},
            "message": {
                "attachment": {
                    "type": "file",
                    "payload": {
                        "url": url
                    }
                }
            }
        }
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(self.access_key)
        return Facebook.send_request(request, url)

    def send_quick_replies(self, text, buttons_text, buttons_action):
        request = {
            "recipient": {"id": self.recipient},
            "message": {
                "text": text,
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": text,
                        "payload": payload
                    } for text, payload in zip(buttons_text, buttons_action)
                    ]
            }
        }
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(self.access_key)
        return Facebook.send_request(request, url)

    @staticmethod
    def send_request(request, url):
        json_request = json.dumps(request)
        headers = {'Content-type': 'application/json'}
        response = requests.post(
            url,
            data=json_request,
            headers=headers
        )
        L.log("Sent message {0}, facebook response: {1}".format(json_request, response.text))
        return response.status_code == 200

    def get_user_context(self):
        url = 'https://graph.facebook.com/v2.8/{0}?access_token={1}'
        rep = requests.get(url.format(self.recipient, self.access_key))
        response_json = json.loads(rep.text)
        print(response_json)
        language = response_json["locale"].split('_')[0]
        name = response_json["first_name"]
        return name, language

    def send_url_button(self, text, titles, urls):
        request = {
            "recipient": {"id": self.recipient},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": [
                            {
                                "type": "web_url",
                                "title": title,
                                "url": url
                            }
                            for title,url in zip(titles, urls)
                            ]
                    }
                }
            }
        }
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(self.access_key)
        return Facebook.send_request(request, url)

    def send_image(self, image_url):
        config = ConfigParser()
        file = os.path.dirname(os.path.abspath(__file__)) + "/../../common.cfg"
        config.read(file)
        media_server_base = config.get("facebook", "media_server")
        if media_server_base[-1] == "/":
            media_server_base = media_server_base[:-1]
        if image_url[0]  == "/":
            image_url = image_url[1:]
        image_full_url = "{0}/{1}".format(media_server_base, image_url)

        request = {
            "recipient": {"id": self.recipient},
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": image_full_url
                    }
                }
            }
        }
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(self.access_key)
        return Facebook.send_request(request, url)


    def send_url(self, titles, text, urls, images):
        request = {
            "recipient": {"id": self.recipient},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                # todo: handle images server and mapping
                                "title": title,
                                "subtitle": "",
                                "image_url": image,
                                "default_action": {
                                    "type": "web_url",
                                    "url": url,
                                    "messenger_extensions": False,
                                    "webview_height_ratio": "tall",
                                },

                            }
                            for title, url, image in zip(titles, urls, images)
                            ]
                    }
                }
            }
        }
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(self.access_key)
        return Facebook.send_request(request, url)

    def send_text(self, text):
        request = {
            "recipient": {
                "id": self.recipient
            },
            "message": {
                "text": text
            }
        }
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(self.access_key)
        return Facebook.send_request(request, url)

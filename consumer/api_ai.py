import apiai
import json
from configparser import ConfigParser
import os

def parse_text(message, language):
    config = ConfigParser()
    file = os.path.dirname(os.path.abspath(__file__)) + "/../../common.cfg"
    config.read(file)
    nlu_access_token = config.get("NLU", "access_token_en")
    client = apiai.ApiAI(nlu_access_token)
    request = client.text_request()
    request.query = message
    response = json.loads(request.getresponse().read())

    return response

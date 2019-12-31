import json
import requests

class MeLog():
    def __init__(self, configfile="./config.json"):
        with open(configfile, "r") as f:
            self.config = json.load(f)

    def postNewLog(self, data):
        url = f"{self.config.get('api').get('endpoint')}/api/v1/melogs"
        headers = {"Authorization": f"Bearer {self.config.get('token').get('access_token')}"}
        r = requests.post(url, headers=headers, json=data)
        return r


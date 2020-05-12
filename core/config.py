import json

config_json = json.load(open("/home/myerfire/Myaer/config.json"))

class Config():
    def __init__(self):
        self.token = config_json["keys"]["token"]
        self.hypixel_api_key = config_json["keys"]["hypixel"]
        self.status_log_channel = config_json["channels"]["status_log_channel"]

import json


class Config:
    def __init__(self):
        with open("config.json") as config:
            config = json.load(config)
        self.token = config["token"]
        self.default_prefix = config["default_prefix"]
        self.owner = config["owner_id"]
        self.channels = Channels(config["channels"])
        self.keys = Keys(config["keys"])

    def get_owner(self, bot):
        self.owner = bot.get_user(self.owner)


class Channels:
    def __init__(self, channels):
        self.events = channels["events"]
        self.status = channels["status"]
        self.guilds = channels["guilds"]

    def get(self, bot):
        self.events = bot.get_channel(self.events)
        self.status = bot.get_channel(self.status)
        self.guilds = bot.get_channel(self.guilds)


class Keys:
    def __init__(self, keys):
        self.hypixel = keys["hypixel"]
        self.ksoft = keys["ksoft"]
        self.genius = keys["genius"]

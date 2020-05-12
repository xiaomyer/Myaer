import aiohttp
from core.config import Config
import json
from core.minecraft.minecraft import Minecraft

hypixel_api = "https://api.hypixel.net/"

class Hypixel():
    def __init__(self):
        self.config = Config()
        self.minecraft = Minecraft()
        self.hypixel_api_key = self.config.hypixel_api_key

    async def send_request(self, player):
        uuid = (await self.minecraft.get_profile(player))["uuid"]
        async with aiohttp.ClientSession() as session:
            raw = await session.get(f"{hypixel_api}player?key={self.hypixel_api_key}&uuid={uuid}")
            global player_json
            player_json = await raw.json()
        if player_json["success"] and player_json["player"]:
            return player_json
        elif player_json["success"] and player_json["player"] == None:
            raise NameError

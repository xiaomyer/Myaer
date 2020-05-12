"""
MIT License

Copyright (c) 2020 MyerFire

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
            raise NameError(f"Player \"{player}\" does not exist!")

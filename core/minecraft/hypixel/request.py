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
from core.minecraft.request import MojangAPI

hypixel_api = "https://api.hypixel.net/"

class HypixelAPI():
    def __init__(self):
        self.config = Config()
        self.mojang = MojangAPI()
        self.hypixel_api_key = self.config.hypixel_api_key

    async def send_player_request(self, player):
        uuid = (await self.mojang.get_profile(player))["uuid"] # &name= is deprecated for the Hypixel API, so convert name to UUID with Mojang API
        async with aiohttp.ClientSession() as session:
            raw = await session.get(f"{hypixel_api}player?key={self.hypixel_api_key}&uuid={uuid}")
            player_json = await raw.json() # but rather per player
        if player_json["success"] and player_json["player"]:
            return player_json
        elif player_json["success"] and player_json["player"] == None: # Hypixel API still returns "success" even if the player does not exist, hence the more complicated check
            raise NameError(f"Player \"{player}\" does not exist!")

    async def send_player_request_uuid(self, uuid):
        async with aiohttp.ClientSession() as session:
            raw = await session.get(f"{hypixel_api}player?key={self.hypixel_api_key}&uuid={uuid.replace('-','')}")
            player_json = await raw.json()
            if player_json["success"] and player_json["player"]:
                return player_json
            elif player_json["success"] and player_json["player"] == None: # Hypixel API still returns "success" even if the player does not exist, hence the more complicated check
                raise NameError(f"Player \"{player}\" does not exist!")

    async def send_leaderboard_request(self):
        async with aiohttp.ClientSession() as session:
            raw = await session.get(f"{hypixel_api}leaderboards?key={self.hypixel_api_key}")
            leaderboards_json = await raw.json()
        if leaderboards_json["success"]:
            return leaderboards_json
        elif not player_json["success"]:
            return NameError("Something went wrong.") # The only reason there could be an error in retreiving leaderboard data is if the API key is invalid, but that should not be possible. TL;DR: If anything gets here, something went horribly wrong.

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
import json
import re

mojang_api = "https://api.mojang.com/"
mojang_session_server = "https://sessionserver.mojang.com/"

class Minecraft():
    async def get_profile(self, player):
        try:
            async with aiohttp.ClientSession() as session:
                profile = await session.get(f"{mojang_api}users/profiles/minecraft/{player}")
                profile_json = await profile.json()
                profile_data = {
                "name" : profile_json["name"], # Case sensitive display name
                "uuid" : profile_json["id"]
                }
        except Exception: # Mojang API returns wrong mimetype if player does not exist
            try:
                async with aiohttp.ClientSession() as session:
                    profile = await session.get(f"{mojang_session_server}session/minecraft/profile/{re.sub('-', '', player)}") # Mojang session server does not accept UUIDs with "-"
                    profile_json = await profile.json()
                    profile_data = {
                    "name" : profile_json["name"],
                    "uuid" : profile_json["id"]
                    }
            except Exception:
                raise NameError(f"Player \"{player}\" does not exist")

        return profile_data

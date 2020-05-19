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

from core.minecraft.request import MojangAPI
import core.minecraft.hypixel.request
from tinydb import TinyDB, Query, where

class Verification():
    def __init__(self):
        self.hypixel = core.minecraft.hypixel.request.HypixelAPI()

    async def verify(self, discord_id, discord_name, minecraft_uuid):
        db = TinyDB("/home/myerfire/Myaer/core/minecraft/verification/verified.json")
        Users = Query()
        try:
            await self.hypixel.send_player_request_uuid(minecraft_uuid)
        except NameError:
            raise NameError("No Hypixel stats for input UUID.")
        try:
            hypixel_discord_name = core.minecraft.hypixel.request.player_json['player']['socialMedia']['links']['DISCORD']
        except KeyError:
            hypixel_discord_name = None
        if (discord_name != hypixel_discord_name) and (hypixel_discord_name != None):
            raise ValueError("Minecraft account already has verified Discord name on Hypixel.")
        elif discord_name == hypixel_discord_name:
            if db.search(where("discord_id") == discord_id):
                db.update({"minecraft_uuid" : minecraft_uuid}, Users.discord_id == discord_id)
            elif db.search(where("minecraft_uuid") == minecraft_uuid):
                db.remove(Users.minecraft_uuid == minecraft_uuid)
                db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
            else:
                db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
        else:
            raise AttributeError("Does not have Discord name set on Hypixel.")

    async def force_verify(self, discord_id, minecraft_uuid):
        db = TinyDB("/home/myerfire/Myaer/core/minecraft/verification/verified.json")
        Users = Query()
        if db.search(where("discord_id") == discord_id):
            db.update({"minecraft_uuid" : minecraft_uuid}, Users.discord_id == discord_id)
        elif db.search(where("minecraft_uuid") == minecraft_uuid):
            db.remove(Users.minecraft_uuid == minecraft_uuid)
            db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
        else:
            db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})

    async def unverify(self, discord_id):
        db = TinyDB("/home/myerfire/Myaer/core/minecraft/verification/verified.json")
        Users = Query()
        if db.search(where("discord_id") == discord_id):
            saved_data = db.search(where("discord_id") == discord_id)
            db.remove(Users.discord_id == discord_id)
            return saved_data
        else:
            print("not verified")
            raise NameError("User is not verified.")

    async def find_uuid(self, discord_id):
        db = TinyDB("/home/myerfire/Myaer/core/minecraft/verification/verified.json")
        Users = Query()
        try:
            return db.search(where("discord_id") == discord_id)
        except:
            return None

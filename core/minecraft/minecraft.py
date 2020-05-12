import aiohttp
import json

mojang_api = "https://api.mojang.com/"
mojang_api_users_profiles_minecraft = f"{mojang_api}users/profiles/minecraft/"

class Minecraft():
    async def get_profile(self, player):
        async with aiohttp.ClientSession() as session:
            profile = await session.get(f"{mojang_api_users_profiles_minecraft}{player}")
            profile_json = await profile.json()
            profile_data = {
            "name" : profile_json["name"],
            "uuid" : profile_json["id"]
            }
        return profile_data

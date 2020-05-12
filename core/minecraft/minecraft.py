import aiohttp
import json

mojang_api = "https://api.mojang.com/"
mojang_api_users_profiles_minecraft = f"{mojang_api}users/profiles/minecraft/"

class Minecraft():
    async def get_profile(self, player):
        try:
            async with aiohttp.ClientSession() as session:
                profile = await session.get(f"{mojang_api_users_profiles_minecraft}{player}")
                profile_json = await profile.json()
                profile_data = {
                "name" : profile_json["name"],
                "uuid" : profile_json["id"]
                }
        except Exception:
            raise NameError(f"Player \"{player}\" does not exist")
        return profile_data

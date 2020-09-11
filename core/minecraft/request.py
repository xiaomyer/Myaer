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
from ratelimit import limits

MOJANG_API = "https://api.mojang.com/"
MOJANG_SESSION_SERVER = "https://sessionserver.mojang.com/"


mojang_request = aiohttp.ClientSession()


@limits(calls=550, period=600)  # mojang ratelimit is 600 requests per 10 minutes, this is to be safe
async def get_profile(player):  # When input could be name or UUID
    try:
        return await get_profile_uuid(player)
    except NameError:
        try:
            return await get_profile_name(player)
        except NameError:
            raise NameError(f"Invalid player name or UUID {player}")


@limits(calls=550, period=600)  # mojang ratelimit is 600 requests per 10 minutes, this is to be safe
async def get_profile_name(player):  # When input is name
    try:
        profile = await mojang_request.get(f"{MOJANG_API}users/profiles/minecraft/{player}")
        profile_json = await profile.json()
        profile_data = {
            "name": profile_json["name"],  # Case sensitive display name
            "uuid": profile_json["id"]
        }
    except Exception:  # Mojang API returns wrong mimetype if player does not exist
        raise NameError(f"Player \"{player}\" does not exist")
    return profile_data


@limits(calls=550, period=600)  # mojang ratelimit is 600 requests per 10 minutes, this is to be safe
async def get_profile_uuid(uuid):  # When input is only UUID
    try:
        profile = await mojang_request.get(
            f"{MOJANG_SESSION_SERVER}session/minecraft/profile/{uuid.replace('-', '')}")  # Mojang session server does not accept UUIDs with "-"
        profile_json = await profile.json()
        profile_data = {
            "name": profile_json["name"],
            "uuid": profile_json["id"]
        }
    except Exception:
        raise NameError(f"Invalid UUID \"{uuid}\"")
    return profile_data


@limits(calls=550, period=600)  # mojang ratelimit is 600 requests per 10 minutes, this is to be safe
async def get_name_history_uuid(player):
    try:
        name_history = []
        name_history_raw = await mojang_request.get(f"{MOJANG_API}user/profiles/{player}/names")
        name_history_json = await name_history_raw.json()
        for name in name_history_json:
            try:
                name_history.append([name["name"], name["changedToAt"]])
            except KeyError:
                name_history.append([name["name"], None])  # First name has no changedToAt key
    except Exception:
        raise NameError(f"Invalid UUID \"{player}\"")
    return name_history

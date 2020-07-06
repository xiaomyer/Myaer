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

from tinydb import Query, where
from tinydb.operations import delete

import core.caches.static
from core.exceptions import HypixelDiscordNotMatching, NoHypixelDiscord


async def get_config(user_id):
    result = core.caches.static.users_db_cache.search(where("user_id") == user_id)
    if result:
        return result[0]
    else:
        return None


async def set_key(user_id, key, data):
    Users = Query()
    result = core.caches.static.users_db_cache.search(where("user_id") == user_id)
    if result:
        core.caches.static.users_db_cache.update({f"{key}": data}, Users.user_id == user_id)
    else:
        core.caches.static.users_db_cache.insert({"user_id": user_id, f"{key}": data})


async def minecraft_verify(user_id, discord_name, minecraft_uuid, hypixel_discord):
    Users = Query()
    if (discord_name != hypixel_discord) and (hypixel_discord is not None):
        raise HypixelDiscordNotMatching
    elif discord_name == hypixel_discord:
        if core.caches.static.users_db_cache.search(where("user_id") == user_id):
            core.caches.static.users_db_cache.update({"minecraft_uuid": minecraft_uuid}, Users.user_id == user_id)
        elif core.caches.static.users_db_cache.search(where("minecraft_uuid") == minecraft_uuid):
            core.caches.static.users_db_cache.update(delete("minecraft_uuid"), Users.user_id == user_id)
            core.caches.static.users_db_cache.insert({"user_id": user_id, "minecraft_uuid": minecraft_uuid})
        else:
            core.caches.static.users_db_cache.insert({"user_id": user_id, "minecraft_uuid": minecraft_uuid})
    else:
        raise NoHypixelDiscord


async def minecraft_force_verify(user_id, minecraft_uuid):
    Users = Query()
    if core.caches.static.users_db_cache.search(where("user_id") == user_id):
        core.caches.static.users_db_cache.update({"minecraft_uuid": minecraft_uuid}, Users.user_id == user_id)
    elif core.caches.static.users_db_cache.search(where("minecraft_uuid") == minecraft_uuid):
        core.caches.static.users_db_cache.update(delete("minecraft_uuid"), Users.user_id == (
            core.caches.static.users_db_cache.search(where("minecraft_uuid") == minecraft_uuid))[0]["minecraft_uuid"])
        core.caches.static.users_db_cache.insert({"user_id": user_id, "minecraft_uuid": minecraft_uuid})
    else:
        core.caches.static.users_db_cache.insert({"user_id": user_id, "minecraft_uuid": minecraft_uuid})


async def reset_key(user_id, key):
    Users = Query()
    result = core.caches.static.users_db_cache.search(where("user_id") == user_id)
    if result:
        saved_data = result if result[0].get(f"{key}", None) else None
        if saved_data:
            core.caches.static.users_db_cache.update(delete(f"{key}"), Users.user_id == user_id)
            return saved_data[0] if saved_data[0].get(f"{key}", None) else None
        else:
            return None
    else:
        return None

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

import core.caches.static
from tinydb import Query, where
from tinydb.operations import delete

async def get_config(guild_id):
	result = core.caches.static.guild_db_cache.search(where("guild_id") == guild_id)
	if result:
		return result[0]
	else: return None

async def set_key(guild_id, key, data):
	Guilds = Query()
	result = core.caches.static.guild_db_cache.search(where("guild_id") == guild_id)
	if result:
		core.caches.static.guild_db_cache.update({f"{key}" : data}, Guilds.guild_id == guild_id)
	else:
		core.caches.static.guild_db_cache.insert({"guild_id" : guild_id, f"{key}" : data})

async def reset_key(guild_id, key):
	Guilds = Query()
	result = core.caches.static.guild_db_cache.search(where("guild_id") == guild_id)
	if result:
		saved_data = result if result[0].get(f"{key}", None) else None
		if saved_data:
			core.caches.static.guild_db_cache.update(delete(f"{key}"), Guilds.guild_id == guild_id)
			return saved_data[0] if saved_data[0].get(f"{key}", None) else None
		else: return None
	else: return None

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
import time
from tinydb import TinyDB, Query, where

async def find_player_data(uuid):
	result = core.caches.static.players_cache_db_cache.search(where("uuid") == uuid)
	if result:
		return result[0]["data"] if (time.time()) - result[0]["time"] < 1800 else None # cached for 30 minutes
	else: return None

async def save_player_data(uuid, player_data):
	db = TinyDB("core/caches/players.json")
	Players = Query()
	if core.caches.static.players_cache_db_cache.search(where("uuid") == uuid):
		db.update({"time" : time.time(), "data" : player_data}, Players.uuid == uuid)
		core.caches.static.players_cache_db_cache.update({"time" : time.time(), "data" : player_data}, Players.uuid == uuid)
	elif core.caches.static.players_cache_db_cache.search(where("data") == player_data):
		db.remove(Players.data == player_data)
		db.insert({"uuid" : uuid, "time" : time.time(), "data" : player_data})
		core.caches.static.players_cache_db_cache.remove(Players.data == player_data)
		core.caches.static.players_cache_db_cache.insert({"uuid" : uuid, "time" : time.time(), "data" : player_data})
	else:
		db.insert({"uuid" : uuid, "time" : time.time(), "data" : player_data})
		core.caches.static.players_cache_db_cache.insert({"uuid" : uuid, "time" : time.time(), "data" : player_data})

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
import core.config.config
from ratelimit import limits
import core.minecraft.request

hypixel_api = "https://api.hypixel.net/"

@limits(calls = 100, period = 60) # hypixel ratelimit is 120/min, this is to be safe
async def get_player(player):
	uuid = (await core.minecraft.request.get_profile(player))["uuid"] # &name= is deprecated for the Hypixel API, so convert name to UUID with Mojang API
	async with aiohttp.ClientSession() as session:
		raw = await session.get(f"{hypixel_api}player?key={core.config.config.hypixel_api_key}&uuid={uuid}")
		player_json = await raw.json()
	if player_json["success"] and player_json["player"]:
		return player_json
	elif player_json["success"] and player_json["player"] is None: # Hypixel API still returns "success" even if the player does not exist, hence the more complicated check
		raise NameError(f"Player \"{player}\" does not exist!")

@limits(calls = 100, period = 60) # hypixel ratelimit is 120/min, this is to be safe
async def get_player_uuid(uuid):
	async with aiohttp.ClientSession() as session:
		raw = await session.get(f"{hypixel_api}player?key={core.config.config.hypixel_api_key}&uuid={uuid.replace('-','')}")
		player_json = await raw.json()
		if player_json["success"] and player_json["player"]:
			return player_json
		elif player_json["success"] and player_json["player"] is None: # Hypixel API still returns "success" even if the player does not exist, hence the more complicated check
			raise NameError(f"Player \"{uuid}\" does not exist!")

@limits(calls = 100, period = 60) # hypixel ratelimit is 120/min, this is to be safe
async def get_leaderboards():
	async with aiohttp.ClientSession() as session:
		raw = await session.get(f"{hypixel_api}leaderboards?key={core.config.config.hypixel_api_key}")
		leaderboards_json = await raw.json()
	if leaderboards_json["success"]:
		return leaderboards_json
	elif not leaderboards_json["success"]:
		return NameError("Something went wrong.") # The only reason there could be an error in retreiving leaderboard data is if the API key is invalid, but that should not be possible. TL;DR: If anything gets here, something went horribly wrong.

@limits(calls = 100, period = 60) # hypixel ratelimit is 120/min, this is to be safe
async def get_guild_by_uuid(uuid):
	async with aiohttp.ClientSession() as session:
		raw = await session.get(f"{hypixel_api}guild?key={core.config.config.hypixel_api_key}&player={uuid}")
		player_guild_json = await raw.json()
	if player_guild_json["success"] and player_guild_json["guild"]:
		return player_guild_json
	elif player_guild_json["success"] and player_guild_json["guild"] is None:
		raise NameError(f"Player \"{uuid}\" does not exist!")

@limits(calls = 100, period = 60) # hypixel ratelimit is 120/min, this is to be safe
async def get_guild_by_name(guild):
	async with aiohttp.ClientSession() as session:
		raw = await session.get(f"{hypixel_api}guild?key={core.config.config.hypixel_api_key}&name={guild}")
		player_guild_json = await raw.json()
	if player_guild_json["success"] and player_guild_json["guild"]:
		return player_guild_json
	elif player_guild_json["success"] and player_guild_json["guild"] is None:
		raise NameError(f"Player \"{uuid}\" does not exist!")

@limits(calls = 100, period = 60) # hypixel ratelimit is 120/min, this is to be safe
async def get_friends_by_uuid(uuid):
	async with aiohttp.ClientSession() as session:
		raw = await session.get(f"{hypixel_api}friends?key={core.config.config.hypixel_api_key}&uuid={uuid}")
		player_friends_json = await raw.json()
	if player_friends_json["success"] and player_friends_json["records"]:
		return player_friends_json
	elif player_friends_json["success"] and player_friends_json["records"] is None:
		raise NameError(f"Player \"{uuid}\" does not exist!")

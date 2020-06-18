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
from discord.ext import commands
import discord
import core.minecraft.request
import core.minecraft.hypixel.player
from tinydb import TinyDB, Query, where

user_converter = commands.UserConverter()

async def verify(discord_id, discord_name, minecraft_uuid, hypixel_discord):
	Users = Query()
	if (discord_name != hypixel_discord) and (hypixel_discord is not None):
		raise ValueError("Minecraft account already has verified Discord name on Hypixel.")
	elif discord_name == hypixel_discord:
		if core.caches.static.verified_db_cache.search(where("discord_id") == discord_id):
			core.caches.static.verified_db_cache.update({"minecraft_uuid" : minecraft_uuid}, Users.discord_id == discord_id)
		elif core.caches.static.verified_db_cache.search(where("minecraft_uuid") == minecraft_uuid):
			core.caches.static.verified_db_cache.remove(Users.minecraft_uuid == minecraft_uuid)
			core.caches.static.verified_db_cache.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
		else:
			core.caches.static.verified_db_cache.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
	else:
		raise AttributeError("Does not have Discord name set on Hypixel.")

async def force_verify(discord_id, minecraft_uuid):
	Users = Query()
	if core.caches.static.verified_db_cache.search(where("discord_id") == discord_id):
		core.caches.static.verified_db_cache.update({"minecraft_uuid" : minecraft_uuid}, Users.discord_id == discord_id)
	elif core.caches.static.verified_db_cache.search(where("minecraft_uuid") == minecraft_uuid):
		db.remove(Users.minecraft_uuid == minecraft_uuid)
		db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
		core.caches.static.verified_db_cache.remove(Users.minecraft_uuid == minecraft_uuid)
		core.caches.static.verified_db_cache.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
	else:
		db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
		core.caches.static.verified_db_cache.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})

async def unverify(discord_id):
	Users = Query()
	if core.caches.static.verified_db_cache.search(where("discord_id") == discord_id):
		saved_data = core.caches.static.verified_db_cache.search(where("discord_id") == discord_id)
		core.caches.static.verified_db_cache.remove(Users.discord_id == discord_id)
		return saved_data
	else:
		raise NameError("User is not verified.")

async def find_uuid(discord_id):
	return core.caches.static.verified_db_cache.search(where("discord_id") == discord_id)

async def parse_input(ctx, input):
	try:
		player_discord = await user_converter.convert(ctx, input)
	except discord.ext.commands.errors.BadArgument:
		player_discord = None
	try:
		if player_discord and (player_discord.mentioned_in(ctx.message) or input.isdigit()): # if input is a discord id
			db_data = (await find_uuid(player_discord.id))
			player_data = {
				"player_formatted_name" : (await core.minecraft.request.get_profile((db_data[0]["minecraft_uuid"])))["name"],
				"minecraft_uuid" : db_data[0]["minecraft_uuid"]
			}
			return player_data
		else:
			try:
				player_info = await core.minecraft.request.get_profile(input)
				player_data = {
					"player_formatted_name" : player_info["name"],
					"minecraft_uuid" : player_info["uuid"]
				}
				return player_data
			except NameError:
				raise NameError
	except IndexError:
		raise AttributeError("Member not verified")
		return

async def database_lookup_uuid(discord_id):
	try:
		db_data = await find_uuid(discord_id)
		return db_data[0]["minecraft_uuid"]
	except IndexError:
		return None # not found in database

async def database_lookup(discord_id):
	try:
		db_data = await find_uuid(discord_id)
		player_data = {
			"player_formatted_name" : (await core.minecraft.request.get_profile((db_data[0]["minecraft_uuid"])))["name"],
			"minecraft_uuid" : db_data[0]["minecraft_uuid"]
		}
		return player_data
	except IndexError:
		return None # not found in database

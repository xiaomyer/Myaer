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

from discord.ext import commands
import discord
import core.minecraft.request
import core.minecraft.hypixel.player
from tinydb import TinyDB, Query, where

user_converter = commands.UserConverter()

async def verify(discord_id, discord_name, minecraft_uuid):
	db = TinyDB("core/minecraft/verification/verified.json")
	Users = Query()
	try:
		player_json = await core.minecraft.hypixel.player.get_player_data(minecraft_uuid)
	except NameError:
		raise NameError("No Hypixel stats for input.")
	if (discord_name != player_json["social_media"]["discord"]) and (player_json["social_media"]["discord"] is not None):
		raise ValueError("Minecraft account already has verified Discord name on Hypixel.")
	elif discord_name == player_json["social_media"]["discord"]:
		if db.search(where("discord_id") == discord_id):
			db.update({"minecraft_uuid" : minecraft_uuid}, Users.discord_id == discord_id)
		elif db.search(where("minecraft_uuid") == minecraft_uuid):
			db.remove(Users.minecraft_uuid == minecraft_uuid)
			db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
		else:
			db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
	else:
		raise AttributeError("Does not have Discord name set on Hypixel.")

async def force_verify(discord_id, minecraft_uuid):
	db = TinyDB("core/minecraft/verification/verified.json")
	Users = Query()
	if db.search(where("discord_id") == discord_id):
		db.update({"minecraft_uuid" : minecraft_uuid}, Users.discord_id == discord_id)
	elif db.search(where("minecraft_uuid") == minecraft_uuid):
		db.remove(Users.minecraft_uuid == minecraft_uuid)
		db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})
	else:
		db.insert({"discord_id" : discord_id, "minecraft_uuid" : minecraft_uuid})

async def unverify(discord_id):
	db = TinyDB("core/minecraft/verification/verified.json")
	Users = Query()
	if db.search(where("discord_id") == discord_id):
		saved_data = db.search(where("discord_id") == discord_id)
		db.remove(Users.discord_id == discord_id)
		return saved_data
	else:
		raise NameError("User is not verified.")

async def find_uuid(discord_id):
	db = TinyDB("core/minecraft/verification/verified.json")
	return db.search(where("discord_id") == discord_id)

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

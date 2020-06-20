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

import core.caches.leaderboards
from discord.ext import commands
import datetime
import discord
import humanfriendly
import core.minecraft.hypixel.leaderboards
import core.static
import core.minecraft.hypixel.static
import sys
import traceback
import time

class LeaderboardCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name = "leaderboards", aliases = ["lb", "leaderboard"], invoke_without_command = True)
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def leaderboards(self, ctx):
		return

# Bedwars

	@leaderboards.group(name = "bedwars", aliases = ["bw"], invoke_without_command = True)
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def bedwars(self, ctx):
		await ctx.channel.trigger_typing()
		leaderboards_cache = await core.caches.leaderboards.find_leaderboards_data("bedwars_level")
		if leaderboards_cache:
			valid = True if (time.time()) - leaderboards_cache["time"] < 86400 else False
		else:
			valid = False
		if valid:
			bedwars_level_leaderboard_string = leaderboards_cache["leaderboards"]
		else:
			leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
			index = 0
			bedwars_level_leaderboard_string = []
			for player in (leaderboards_json["bedwars"]["level"]):
				player_json = await core.minecraft.hypixel.player.get_player_data(player)
				bedwars_level_leaderboard_string.append(f"""#{index + 1} - {f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}" if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star} {player_json['name']}]"} - {(await core.minecraft.hypixel.static.get_ratio(player_json["bedwars"]["final_kills"], player_json["bedwars"]["final_deaths"]))} FKDR""",)
				index += 1
		await core.caches.leaderboards.save_leaderboards_data("bedwars_level", bedwars_level_leaderboard_string)
		joined_string = "\n".join(bedwars_level_leaderboard_string)
		bedwars_level_leaderboard_embed = discord.Embed(
			description = f"```{joined_string}```"
		)
		await ctx.send(embed = bedwars_level_leaderboard_embed)

	@bedwars.group(name = "wins", aliases = ["win"], invoke_without_command = True)
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def bedwars_wins(self, ctx):
		await ctx.channel.trigger_typing()
		leaderboards_cache = await core.caches.leaderboards.find_leaderboards_data("bedwars_wins")
		if leaderboards_cache:
			valid = True if (time.time()) - leaderboards_cache["time"] < 86400 else False
		else:
			valid = False
		if valid:
			bedwars_overall_wins_leaderboard_string = leaderboards_cache["leaderboards"]
		else:
			leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
			index = 0
			bedwars_overall_wins_leaderboard_string = []
			for player in (leaderboards_json["bedwars"]["wins"]["overall"]):
				player_json = await core.minecraft.hypixel.player.get_player_data(player)
				bedwars_overall_wins_leaderboard_string.append(f"""#{index + 1} - {f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}" if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star} {player_json['name']}]"} - {player_json['bedwars']['wins']} wins""")
				index += 1
		await core.caches.leaderboards.save_leaderboards_data("bedwars_wins", bedwars_overall_wins_leaderboard_string)
		joined_string = "\n".join(bedwars_overall_wins_leaderboard_string)
		bedwars_overall_wins_leaderboard_embed = discord.Embed(
			description = f"```{joined_string}```"
		)
		await ctx.send(embed = bedwars_overall_wins_leaderboard_embed)

	@bedwars_wins.command(name = "weekly")
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def bedwars_weekly_wins(self, ctx):
		await ctx.channel.trigger_typing()
		leaderboards_cache = await core.caches.leaderboards.find_leaderboards_data("bedwars_weekly_wins")
		if leaderboards_cache:
			valid = True if (time.time()) - leaderboards_cache["time"] < 86400 else False
		else:
			valid = False
		if valid:
			bedwars_weekly_wins_leaderboard_string = leaderboards_cache["leaderboards"]
		else:
			leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
			index = 0
			bedwars_weekly_wins_leaderboard_string = []
			for player in (leaderboards_json["bedwars"]["wins"]["weekly"]):
				player_json = await core.minecraft.hypixel.player.get_player_data(player)
				bedwars_weekly_wins_leaderboard_string.append(f"""#{index + 1} - {f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}" if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star}] {player_json['name']}"}""")
				index += 1
		await core.caches.leaderboards.save_leaderboards_data("bedwars_weekly_wins", bedwars_weekly_wins_leaderboard_string)
		joined_string = "\n".join(bedwars_weekly_wins_leaderboard_string)
		bedwars_weekly_wins_leaderboard_embed = discord.Embed(
			description = f"```{joined_string}```"
		)
		await ctx.send(embed = bedwars_weekly_wins_leaderboard_embed)

	@bedwars.group(name = "finals", aliases = ["final"], invoke_without_command = True)
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def bedwars_finals(self, ctx):
		await ctx.channel.trigger_typing()
		leaderboards_cache = await core.caches.leaderboards.find_leaderboards_data("bedwars_finals")
		if leaderboards_cache:
			valid = True if (time.time()) - leaderboards_cache["time"] < 86400 else False
		else:
			valid = False
		if valid:
			bedwars_weekly_wins_leaderboard_string = leaderboards_cache["leaderboards"]
		else:
			leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
			index = 0
			bedwars_overall_finals_leaderboard_string = []
			for player in (leaderboards_json["bedwars"]["finals"]["overall"]):
				player_json = await core.minecraft.hypixel.player.get_player_data(player)
				bedwars_overall_finals_leaderboard_string.append(f"""#{index + 1} - {f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}" if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star} {player_json['name']}]"} - {player_json['bedwars']['final_kills']} finals""")
				index += 1
		await core.caches.leaderboards.save_leaderboards_data("bedwars_finals", bedwars_overall_finals_leaderboard_string)
		joined_string = "\n".join(bedwars_overall_finals_leaderboard_string)
		bedwars_overall_finals_leaderboard_embed = discord.Embed(
			description = f"```{joined_string}```"
		)
		await ctx.send(embed = bedwars_overall_finals_leaderboard_embed)

	@bedwars_finals.command(name = "weekly")
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def bedwars_weekly_finals(self, ctx):
		await ctx.channel.trigger_typing()
		leaderboards_cache = await core.caches.leaderboards.find_leaderboards_data("bedwars_weekly_finals")
		if leaderboards_cache:
			valid = True if (time.time()) - leaderboards_cache["time"] < 86400 else False
		else:
			valid = False
		if valid:
			bedwars_weekly_finals_leaderboard_string = leaderboards_cache["leaderboards"]
		else:
			leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
			index = 0
			bedwars_weekly_finals_leaderboard_string = []
			for player in (leaderboards_json["bedwars"]["finals"]["weekly"]):
				player_json = await core.minecraft.hypixel.player.get_player_data(player)
				bedwars_weekly_finals_leaderboard_string.append(f"""#{index + 1} - {f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}" if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star} {player_json['name']}]"}""")
				index += 1
		await core.caches.leaderboards.save_leaderboards_data("bedwars_weekly_finals", bedwars_weekly_finals_leaderboard_string)
		joined_string = "\n".join(bedwars_weekly_finals_leaderboard_string)
		bedwars_weekly_finals_leaderboard_embed = discord.Embed(
			description = f"```{joined_string}```"
		)
		await ctx.send(embed = bedwars_weekly_finals_leaderboard_embed)

def setup(bot):
	bot.add_cog(LeaderboardCommands(bot))
	print("Reloaded cogs.minecraft.hypixel.leaderboards")

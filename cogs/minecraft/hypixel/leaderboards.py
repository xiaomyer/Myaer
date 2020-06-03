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

import asyncio
import core.minecraft.hypixel.leaderboards
import core.static
import datetime
from discord.ext import commands
import discord
import humanfriendly
import core.minecraft.hypixel.static
import core.minecraft.hypixel.player
import sys
import time
import traceback

class LeaderboardCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name = "leaderboards", aliases = ["lb", "leaderboard"], invoke_without_command = True)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def leaderboards(self, ctx):
		return

# Bedwars

	@leaderboards.group(name = "bedwars", aliases = ["bw"], invoke_without_command = True)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def bedwars(self, ctx):
		loading_embed = discord.Embed(
			name = "Loading",
			description = "Loading Bedwars level leaderboard..."
		)
		message = await ctx.send(embed = loading_embed)
		leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
		index = 0
		bedwars_level_leaderboard_embed = discord.Embed(
			name = "Level leaderboard",
			color = ctx.author.color
		)
		for player in (leaderboards_json["bedwars"]["level"]):
			player_json = await core.minecraft.hypixel.player.get_player(player)
			bedwars_level_leaderboard_embed.add_field(
				name = f"#{index + 1}",
				value = f"""**{discord.utils.escape_markdown(f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}") if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star} {player_json['name']}]"} - {(await core.minecraft.hypixel.static.get_ratio(player_json["bedwars"]["final_kills"], player_json["bedwars"]["final_deaths"]))} FKDR**""",
				inline = False
			)
			index += 1
		await message.edit(embed = bedwars_level_leaderboard_embed)

	@bedwars.group(name = "wins", aliases = ["win"], invoke_without_command = True)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def bedwars_wins(self, ctx):
		loading_embed = discord.Embed(
			name = "Loading",
			description = "Loading Bedwars overall wins leaderboard..."
		)
		message = await ctx.send(embed = loading_embed)
		leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
		index = 0
		bedwars_overall_wins_leaderboard_embed = discord.Embed(
			name = "Overall wins leaderboard",
			color = ctx.author.color
		)
		for player in (leaderboards_json["bedwars"]["wins"]["overall"]):
			player_json = await core.minecraft.hypixel.player.get_player(player)
			bedwars_overall_wins_leaderboard_embed.add_field(
				name = f"#{index + 1}",
				value = f"""**{discord.utils.escape_markdown(f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}") if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star} {player_json['name']}]"} - {player_json['bedwars']['wins']} wins**""",
				inline = False
			)
			index += 1
		await message.edit(embed = bedwars_overall_wins_leaderboard_embed)

	@bedwars_wins.command(name = "weekly")
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def bedwars_weekly_wins(self, ctx):
		loading_embed = discord.Embed(
			name = "Loading",
			description = "Loading Bedwars weekly wins leaderboard..."
		)
		message = await ctx.send(embed = loading_embed)
		leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
		index = 0
		bedwars_weekly_wins_leaderboard_embed = discord.Embed(
			name = "Bedwars weekly wins leaderboard",
			color = ctx.author.color
		)
		for player in (leaderboards_json["bedwars"]["wins"]["weekly"]):
			player_json = await core.minecraft.hypixel.player.get_player(player)
			bedwars_weekly_wins_leaderboard_embed.add_field(
				name = f"#{index + 1}",
				value = f"""**{discord.utils.escape_markdown(f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}") if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star}] {player_json['name']}"}**""",
				inline = False
			)
			index += 1
		await message.edit(embed = bedwars_weekly_wins_leaderboard_embed)

	@bedwars.group(name = "finals", aliases = ["final"], invoke_without_command = True)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def bedwars_finals(self, ctx):
		loading_embed = discord.Embed(
			name = "Loading",
			description = "Loading Bedwars overall final kills leaderboard..."
		)
		message = await ctx.send(embed = loading_embed)
		leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
		index = 0
		bedwars_overall_finals_leaderboard_embed = discord.Embed(
			name = "Bedwars overall finals leaderboard",
			color = ctx.author.color
		)
		for player in (leaderboards_json["bedwars"]["finals"]["overall"]):
			player_json = await core.minecraft.hypixel.player.get_player(player)
			bedwars_overall_finals_leaderboard_embed.add_field(
				name = f"#{index + 1}",
				value = f"""**{discord.utils.escape_markdown(f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}") if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star} {player_json['name']}]"} - {player_json['bedwars']['final_kills']} finals**""",
				inline = False
			)
			index += 1
		await message.edit(embed = bedwars_overall_finals_leaderboard_embed)

	@bedwars_finals.command(name = "weekly")
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def bedwars_weekly_finals(self, ctx):
		loading_embed = discord.Embed(
			name = "Loading",
			description = "Loading Bedwars weekly final kills leaderboard..."
		)
		message = await ctx.send(embed = loading_embed)
		leaderboards_json = await core.minecraft.hypixel.leaderboards.get_leaderboards()
		index = 0
		bedwars_weekly_finals_leaderboard_embed = discord.Embed(
			name = "Bedwars weekly finals leaderboard",
			color = ctx.author.color
		)
		for player in (leaderboards_json["bedwars"]["finals"]["weekly"]):
			player_json = await core.minecraft.hypixel.player.get_player(player)
			bedwars_weekly_finals_leaderboard_embed.add_field(
				name = f"#{index + 1}",
				value = f"""**{discord.utils.escape_markdown(f"[{player_json['bedwars']['star']}{core.static.star}] [{player_json['rank_data']['rank']}] {player_json['name']}") if player_json["rank_data"]["rank"] else f"[{player_json['bedwars']['star']}{core.static.star} {player_json['name']}]"}**""",
				inline = False
			)
			index += 1
		await message.edit(embed = bedwars_weekly_finals_leaderboard_embed)

	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			cooldown = datetime.timedelta(seconds = error.retry_after)
			cooldown_embed = discord.Embed(
				name = "Cooldown",
				color = ctx.author.color,
				description = f"Leaderboard commands have a cooldown of 60s. Try again in {humanfriendly.format_timespan(cooldown)}"
			)
			await ctx.send(embed = cooldown_embed)

		print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
	bot.add_cog(LeaderboardCommands(bot))
	print("Reloaded cogs.minecraft.hypixel.leaderboards")

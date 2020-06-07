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
import datetime
import discord
import humanfriendly
import math
import core.static
import core.minecraft.static
import core.minecraft.hypixel.static

mc_heads_api = "https://mc-heads.net/"

class Hypixel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name = "hypixel", aliases = ["hp"], invoke_without_command = True)
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def hypixel(self, ctx, *args):
		player_info = await core.minecraft.static.name_handler(ctx, args, get_guild = True)
		if player_info:
			player_data = player_info["player_data"]
			player_json = player_info["player_json"]
		else: return
		player_info_embed = discord.Embed(
			title = f"""**{discord.utils.escape_markdown(f"[{player_json['rank_data']['rank']}] {player_data['player_formatted_name']}" if player_json["rank_data"]["rank"] else player_data["player_formatted_name"])}**""",
			color = int((player_json["rank_data"])["color"], 16) # 16 - hex value
		)
		player_info_embed.set_thumbnail(
			url = core.minecraft.hypixel.static.hypixel_icons["Main"]
		)
		player_info_embed.set_footer(
			text = mc_heads_api,
			icon_url = f"{mc_heads_api}avatar/{player_data['minecraft_uuid']}/100"
		)
		player_info_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Level**__",
			value = f"{player_json['level_data']['level']} ({player_json['level_data']['percentage']}% to {math.trunc((player_json['level_data']['level']) + 1)})"
		)
		player_info_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Karma**__",
			value = f"{(player_json['karma']):,d}"
		)
		player_info_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Achievement Points**__",
			value = f"{(player_json['achievement_points']):,d}"
		)
		player_info_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} First Login**__",
			value = f"{datetime.date.fromtimestamp((player_json['login_times']['first']) / 1000)}"
		)
		player_info_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Last Login**__",
			value =
f"""{datetime.date.fromtimestamp((player_json['login_times']['last']) / 1000)}
({(humanfriendly.format_timespan(((datetime.datetime.now()) - (datetime.datetime.fromtimestamp((player_json['login_times']['last']) / 1000))), max_units = 2))} ago)"""
		)
		if player_json['guild_data']: # checks if player is in a guild
			player_info_embed.add_field(
				name = f"__**{core.static.arrow_bullet_point} Guild**__",
				value = f"""{discord.utils.escape_markdown(f"{player_json['guild_data']['name']} [{player_json['guild_data']['tag']}]" if player_json["guild_data"]["tag"] else f"{player_json['guild_data']['name']}")}""", # checks if player's guild has a tag
				inline = False
			)
		await ctx.send(embed = player_info_embed)

def setup(bot):
	bot.add_cog(Hypixel(bot))
	print("Reloaded cogs.minecraft.hypixel.hypixel")

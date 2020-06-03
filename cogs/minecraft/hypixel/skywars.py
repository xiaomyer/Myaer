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

import core.static
from discord.ext import commands
import discord
import core.minecraft.hypixel.player
import core.minecraft.hypixel.static
import core.minecraft.verification.verification

class SkywarsStats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.user_converter = commands.UserConverter()

	@commands.group(name = "sw", invoke_without_command = True)
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def skywars(self, ctx, *args):
		if len(args):
			try:
				player_data = await core.minecraft.verification.verification.parse_input(ctx, args[0])
			except AttributeError:
				member_not_verified = discord.Embed(
					name = "Member not verified",
					description = f"{args[0]} is not verified. Tell them to do `/mc verify <their-minecraft-ign>`",
					color = ctx.author.color
				)
				member_not_verified.set_footer(
					text = "... with Myaer."
				)
				await ctx.send(embed = member_not_verified)
				return
			except NameError:
				nameerror_embed = discord.Embed(
					name = "Invalid input",
					description = f"\"{args[0]}\" is not a valid username or UUID.",
					color = ctx.author.color
				)
				await ctx.send(embed = nameerror_embed)
				return
		else:
			player_data = await core.minecraft.verification.verification.database_lookup(ctx.author.id)
			if player_data is None:
				unverified_embed = discord.Embed(
					name = "Not verified",
					description = "You have to verify with `/mc verify <minecraft-ign>` first.",
					color = ctx.author.color
				)
				await ctx.send(embed = unverified_embed)
				return
		loading_embed = discord.Embed(
			name = "Loading",
			description = f"Loading {player_data['player_formatted_name']}'s Skywars stats...",
			color = ctx.author.color
		)
		message = await ctx.send(embed = loading_embed)
		try:
			player_json = await core.minecraft.hypixel.player.get_player(player_data["minecraft_uuid"])
		except NameError:
			nameerror_embed = discord.Embed(
				name = "Invalid input",
				description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats.",
				color = ctx.author.color
			)
			await message.edit(embed = nameerror_embed)
			return
		player_stats_embed = discord.Embed(
			title = f"""**{discord.utils.escape_markdown(f"[{player_json['rank_data']['rank']}] {player_data['player_formatted_name']}" if player_json["rank_data"]["rank"] else player_data["player_formatted_name"])}'s Skywars Stats**""",
			color = int((await core.minecraft.hypixel.static.get_skywars_prestige_data(player_json["skywars"]["star"]))["prestige_color"], 16) # 16 - Hex value.
		)
		player_stats_embed.set_thumbnail(
			url = core.minecraft.hypixel.static.hypixel_icons["Skywars"]
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Level**__",
			value = f"{player_json['skywars']['star']} {core.static.star} ({(await core.minecraft.hypixel.static.get_skywars_prestige_data(player_json['skywars']['star']))['prestige']} Prestige)",
			inline = False
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Coins**__",
			value = f"{player_json['skywars']['coins']}"
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Tokens**__",
			value = f"{player_json['skywars']['tokens']}"
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Souls**__",
			value = f"{player_json['skywars']['souls']}"
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Kills**__",
			value = f"{player_json['skywars']['kills']}"
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Deaths**__",
			value = f"{player_json['skywars']['deaths']}"
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} KDR**__",
			value = f"{(await core.minecraft.hypixel.static.get_ratio((player_json['skywars']['kills']), (player_json['skywars']['deaths'])))}"
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Wins**__",
			value = f"{player_json['skywars']['wins']}"
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Losses**__",
			value = f"{player_json['skywars']['losses']}"
		)
		player_stats_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} WLR**__",
			value = f"{(await core.minecraft.hypixel.static.get_ratio((player_json['skywars']['wins']), (player_json['skywars']['losses'])))}"
		)
		await message.edit(embed = player_stats_embed)

def setup(bot):
	bot.add_cog(SkywarsStats(bot))
	print("Reloaded cogs.minecraft.hypixel.skywars")

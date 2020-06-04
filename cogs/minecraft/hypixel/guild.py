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
import core.minecraft.hypixel.guild
import core.minecraft.hypixel.static
import core.static
import core.minecraft.verification.verification

class Guild(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name = "guild", aliases = ["g"], invoke_without_command = True)
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def guild(self, ctx, *args):
		if len(args):
			try:
				player_data = await core.minecraft.verification.verification.parse_input(ctx, args[0])
			except AttributeError:
				member_not_verified = discord.Embed(
					name = "Member not verified",
					description = f"{args[0]} is not verified. Tell them to do `/mc verify <their-minecraft-ign>`",
					color = ctx.author.color
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
			description = f"Loading {player_data['player_formatted_name']}'s guild data...",
			color = ctx.author.color
		)
		message = await ctx.send(embed = loading_embed)
		try:
			guild_json = await core.minecraft.hypixel.guild.get_guild_data_uuid(player_data["minecraft_uuid"])
		except NameError:
			nameerror_embed = discord.Embed(
				name = "Invalid input",
				description = f"{player_data['player_formatted_name']} is not in a guild"
			)
			await message.edit(embed = nameerror_embed)
			return
		player_guild_embed = discord.Embed(
			name = "Player guild",
			color = int((guild_json['color']), 16) if guild_json['color'] else ctx.author.color
		)
		player_guild_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Name**__",
			value = f"{guild_json['name']}"
		)
		if guild_json["tag"]:
			player_guild_embed.add_field(
				name = f"__**{core.static.arrow_bullet_point} Tag**__",
				value = f"[{guild_json['tag']}]"
			)
		await message.edit(embed = player_guild_embed)
def setup(bot):
	bot.add_cog(Guild(bot))
	print("Reloaded cogs.minecraft.hypixel.guild")

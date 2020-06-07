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
import math
import core.static
import core.minecraft.static
import core.minecraft.hypixel.static

class Guild(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name = "guild", aliases = ["g"], invoke_without_command = True)
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def guild(self, ctx, *args):
		player_info = await core.minecraft.static.name_handler(ctx, args)
		if player_info:
			player_data = player_info["player_data"]
			player_json = player_info["player_json"]
		else: return
		try:
			guild_json = await core.minecraft.hypixel.static.get_guild_data_uuid(player_data["minecraft_uuid"])
		except NameError:
			nameerror_embed = discord.Embed(
				name = "Invalid input",
				description = f"{player_data['player_formatted_name']} is not in a guild"
			)
			await message.edit(embed = nameerror_embed)
			return
		player_guild_embed = discord.Embed(
			name = "Player guild",
			title = f"""{discord.utils.escape_markdown(f"{guild_json['name']} [{guild_json['tag']}]") if guild_json["tag"] else f"{guild_json['name']}"}""",
			color = int((guild_json['color']), 16) if guild_json['color'] else ctx.author.color
		)
		player_guild_embed.add_field(
			name = f"__**{core.static.arrow_bullet_point} Level**__",
			value = f"{guild_json['level_data']['level']} ({guild_json['level_data']['percentage']}% to {math.trunc((guild_json['level_data']['level'])) + 1})"
		)
		await ctx.send(embed = player_guild_embed)
def setup(bot):
	bot.add_cog(Guild(bot))
	print("Reloaded cogs.minecraft.hypixel.guild")

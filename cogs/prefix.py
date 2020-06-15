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
import core.config
import discord
import core.prefix
from tinydb import TinyDB, Query, where

class Prefix(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name = "prefix", invoke_without_command = True)
	@commands.guild_only()
	async def prefix(self, ctx):
		db_data = await core.prefix.get_prefix(ctx.guild.id)
		prefix = db_data[0]["prefix"] if db_data else None
		prefix_embed = discord.Embed(
			name = "Prefix",
			description = f"This server's current prefix is `{prefix}`" if prefix else f"This server is using the default prefix, `{core.config.default_prefix}`"
		)
		await ctx.send(embed = prefix_embed)

	@prefix.command(name = "set")
	@commands.has_guild_permissions(manage_guild = True)
	@commands.guild_only()
	async def set_prefix(self, ctx, prefix):
		if prefix == core.config.default_prefix: # cannot set to default prefix
			default_embed = discord.Embed(
				name = "Cannot set prefix to default",
				description = "You cannot set a guild's custom prefix to the default prefix"
			)
			await ctx.send(embed = default_embed)
		elif len(prefix) < 10:
			await core.prefix.set_prefix(ctx.guild.id, prefix)
			set_embed = discord.Embed(
				name = "Set prefix",
				description = f"Set this server's prefix to `{prefix}`"
			)
			await ctx.send(embed = set_embed)
		else:
			too_long_embed = discord.Embed(
				name = "Too long",
				description = "Prefixes should not be that long. Try a shorter one"
			)
			await ctx.send(embed = too_long_embed)

	@prefix.command(name = "reset")
	@commands.has_guild_permissions(manage_guild = True)
	@commands.guild_only()
	async def reset_prefix(self, ctx):
		resetting_embed = discord.Embed(
			name = "Resetting prefix",
			description = "Resetting custom guild prefix..."
		)
		message = await ctx.send(embed = resetting_embed)
		reset_data = await core.prefix.reset_prefix(ctx.guild.id)
		reset_embed = discord.Embed(
			name = "Reset prefix",
			description = f"Reset this server's prefix from `{reset_data[0]['prefix']}` to `{core.config.default_prefix}`"
		)
		await message.edit(embed = reset_embed)

def setup(bot):
	bot.add_cog(Prefix(bot))
	print("Reloaded cogs.prefix")

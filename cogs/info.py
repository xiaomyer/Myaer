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

import datetime
from discord.ext import commands
import discord
import humanfriendly
import core.static.static

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name = "user", alises = ["member"])
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def user(self, ctx, *args):
		if bool(len(args)):
			try:
				user = await ctx.bot.member_converter.convert(ctx, args[0])
			except commands.BadArgument:
				user = None # could be a User and not a Member
			try:
				user = await ctx.bot.user_converter.convert(ctx, args[0]) if not user else user # sets to a User instead of a Member if member object was not found
			except commands.BadArgument: # actual bad argument
				no_user_embed = discord.Embed(
					description = f"Member or user \"{args[0]}\" was not found"
				)
				await ctx.send(embed = no_user_embed)
				return
		else:
			user = ctx.author
		user_embed = discord.Embed(
			color = user.color if isinstance(user, discord.Member) else ctx.author.color,
			timestamp = ctx.message.created_at
		)
		user_embed.add_field(
			name = f"__**{core.static.static.arrow_bullet_point} Account Creation**__",
			value =
f"""{user.created_at.strftime('%m/%d/%Y - %I:%M:%S %p')}
({humanfriendly.format_timespan(datetime.datetime.now() - user.created_at)} ago)"""
		)
		user_embed.set_author(
			name = f"{user.name}#{user.discriminator} ({user.id})",
			icon_url = str(user.avatar_url_as(static_format = "png", size = 2048))
		)
		await ctx.send(embed = user_embed)

def setup(bot):
	bot.add_cog(Info(bot))
	print("Reloaded cogs.info")

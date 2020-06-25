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

class Avatar(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name = "avatar", aliases = ["pfp"])
	@commands.max_concurrency(1, per = commands.BucketType.user)
	async def avatar(self, ctx, *args):
		if bool(len(args)):
			user = await ctx.bot.user_converter.convert(ctx, args[0])
			member = ctx.guild.get_member(user.id)
			color = member.color if bool(member) else ctx.author.color
		else:
			user = ctx.author
			color = ctx.author.color
		avatar_embed = discord.Embed(
			title = f"{user.name}'s Avatar",
			color = color
		)
		avatar_embed.set_image(
			url = str(user.avatar_url_as(static_format = "png", size = 2048))
		)
		await ctx.send(embed = avatar_embed)

def setup(bot):
	bot.add_cog(Avatar(bot))
	print("Reloaded commands.avatar")

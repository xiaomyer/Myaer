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
import random
import core.minecraft.verification.verification

uses_verify = ["minecraft", "bedwars", "duels", "guild", "hypixel", "paintball", "skywars"]

class OnCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command(self, ctx):
		if (str(ctx.command) in uses_verify) and "verify" not in str(ctx.command):
			user_config = await core.config.users.get_config(ctx.author.id)
			if user_config:
				valid = False if (await core.config.users.get_config(ctx.author.id)).get("minecraft_uuid", None) else True
			else:
				valid = True
			if valid:
				if random.randint(0, 100) < 75: # some percent chance that this will be sent
					await ctx.send(
"""**__Note__**: The bot's host machine was reinstalled today, causing all data to be erased (the machine was corrupted). I apologize for any inconvenience."""
					)

def setup(bot):
	bot.add_cog(OnCommand(bot))
	print("Reloaded events.on_command")

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

import discord
from discord.ext import commands
import core.config
import datetime
import humanfriendly
import sys
import traceback

error_log_channel = core.config.error_log_channel

class CommandError(commands.Cog):
	def __init(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		error = getattr(error, "original", error)

		if hasattr(ctx.command, "on_error"):
			return
		ignored = (commands.CommandNotFound)
		if isinstance(error, ignored):
			return

		print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

		error_traceback = "".join(traceback.format_exception(type(error), error, error.__traceback__))
		error_log_channel_object = ctx.bot.get_channel(error_log_channel)
		error_embed = discord.Embed(
			color = ctx.author.color,
			timestamp = ctx.message.created_at,
			title =
f"""Ignoring exception in command {ctx.command}
```{ctx.message.content}```""",
			description =
f"""
{f'in guild `{ctx.guild.name} ({ctx.guild.id})`' if isinstance(ctx.message.channel, discord.TextChannel) else 'in a DM channel'}
invoked by <@!{ctx.author.id}> `({ctx.author.name}#{ctx.author.discriminator}) ({ctx.author.id})`
```{error_traceback}```"""
		)
		await error_log_channel_object.send(embed = error_embed)

# myer, you silly goose! why are you putting this before the check for a local error handler?
# i just want to see how many times there are actual errors
# and i want to see how many times my cooldowns are met

		if (str(ctx.command)).startswith("leaderboards"):
			return

		if isinstance(error, commands.MaxConcurrencyReached):
			concurrency_embed = discord.Embed(
				color = ctx.author.color,
				description = f"{ctx.author.name}, this command is being ratelimited. Try again in a bit"
			)
			await ctx.send(embed = concurrency_embed)

		if isinstance(error, commands.CommandOnCooldown):
			cooldown = datetime.timedelta(seconds = error.retry_after)
			cooldown_embed = discord.Embed(
				color = ctx.author.color,
				description = f"{ctx.author.name}, you are sending commands too fast. Try again in {humanfriendly.format_timespan(cooldown)}"
			)
			await ctx.send(embed = cooldown_embed)

		if isinstance(error, commands.MissingRequiredArgument):
			argument_embed = discord.Embed(
				color = ctx.author.color,
				description = f"{ctx.author.name}, you forgot to provide an input of some sort"
			)
			await ctx.send(embed = argument_embed)

		if isinstance(error, commands.MissingPermissions):
			argument_embed = discord.Embed(
				color = ctx.author.color,
				description = f"{ctx.author.name}, you don't have enough permissions to do that"
			)
			await ctx.send(embed = argument_embed)

def setup(bot):
	bot.add_cog(CommandError(bot))
	print("Reloaded events.command_error")

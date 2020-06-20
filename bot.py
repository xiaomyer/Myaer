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

import core.caches.static
import core.config.config
import datetime
import discord
from discord.ext import commands
import core.config.guilds
import logging
import os
import sys
import traceback

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

async def get_prefix(bot, message):
	if isinstance(message.channel, discord.DMChannel):
		return commands.when_mentioned_or(core.config.config.default_prefix, "myaer", "Myaer")(bot, message)
	guild_config = await core.config.guilds.get_config(message.guild.id)
	if guild_config:
		prefix = guild_config["prefix"] if guild_config.get("prefix") else core.config.config.default_prefix
	else:
		prefix = core.config.config.default_prefix
	return commands.when_mentioned_or(prefix, "myaer ", "Myaer ")(bot, message)

bot = commands.Bot(
	command_prefix = get_prefix,
	owner_id = core.config.config.owner_id
)
bot.default_prefix = core.config.config.default_prefix
bot.hypixel_api_key = core.config.config.hypixel_api_key
bot.status_log_channel = core.config.config.status_log_channel
bot.error_log_channel = core.config.config.error_log_channel
bot.guilds_log_channel = core.config.config.guilds_log_channel
bot.suggestions_channel = core.config.config.suggestions_channel

bot.mc_heads_api = "https://mc-heads.net/"
bot.surgeplay_api = "https://visage.surgeplay.com/"

time_format = "%A, %b %d, %Y - %m/%d/%Y - %I:%M:%S %p"
program_start_time = datetime.datetime.now()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
error_log_channel = core.config.config.error_log_channel

extensions = [os.path.join(dp, f) for dp, dn, fn in os.walk("cogs") for f in fn] + [os.path.join(dp, f) for dp, dn, fn in os.walk("commands") for f in fn] + [os.path.join(dp, f) for dp, dn, fn in os.walk("modules") for f in fn] + [os.path.join(dp, f) for dp, dn, fn in os.walk("events") for f in fn] + ["jishaku"]
for file in extensions[:]:
	if not file.endswith(".py") and file != "jishaku":
		extensions.remove(file)
failed_extensions = []

@bot.event
async def on_ready():
	ready_time = datetime.datetime.now()
	status_log_channel = bot.get_channel(core.config.config.status_log_channel)
	error_log_channel_object = bot.get_channel(error_log_channel)
	print(f"Connection with Discord established at {ready_time.strftime(time_format)}")
	for failed_extension in failed_extensions:
		error_embed = discord.Embed(
			title = f"Failed to load extension {failed_extension['extension']}",
			description = f"```{failed_extension['traceback']}```"
		)
		await error_log_channel_object.send(embed = error_embed)
	await bot.change_presence(activity = discord.Game(name = "/help | /suggest"))
	await status_log_channel.send(f"Logged in at {ready_time.strftime(time_format)} (took {(ready_time - program_start_time).total_seconds()} seconds).")

@bot.event
async def on_error(event, *args, **kwargs):
	error = sys.exc_info()
	error_traceback = "".join(traceback.format_exception(error[0], error[1], error[2]))
	print(error_traceback)
	error_log_channel_object = bot.get_channel(error_log_channel)
	error_embed = discord.Embed(
		title = "Exception",
		description = f"```{error_traceback}```"
	)
	error_embed.set_footer(
		text = (datetime.datetime.now()).strftime(time_format)
	)
	await error_log_channel_object.send(embed = error_embed)

if __name__ == "__main__":
	for extension in extensions:
		try:
			bot.load_extension(((extension.replace("/", "."))[:-3]) if extension.endswith(".py") else extension)
		except Exception as e:
			exception = '{}: {}'.format(type(e).__name__, e)
			print("Failed to load extension {}\n{}".format(extension, exception))
			error_traceback = "".join(traceback.format_exception(type(e), e, e.__traceback__))
			failed_extensions.append({"extension" : extension, "traceback" : error_traceback})

bot.run(core.config.config.token)

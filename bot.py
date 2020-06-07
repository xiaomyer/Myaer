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

import core.config
import datetime
import discord
from discord.ext import commands
import logging
from tinydb import TinyDB, Query, where

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

async def get_prefix(bot, message):
	prefix_data = core.config.prefix_db_cache.search(where("guild_id") == message.guild.id)
	prefix = prefix_data[0]["prefix"] if prefix_data else core.config.default_prefix
	return commands.when_mentioned_or(prefix, "myaer ", "Myaer ")(bot, message)

bot = commands.Bot(
	command_prefix = get_prefix,
	owner_id = 368780147563823114
)

extensions = [
	"jishaku",
	"commands.announcement",
	"cogs.minecraft.hypixel.bedwars",
	"events.command_error",
	"cogs.minecraft.hypixel.duels",
	"cogs.minecraft.hypixel.guild",
	"commands.help",
	"cogs.minecraft.hypixel.hypixel",
	"cogs.minecraft.hypixel.leaderboards",
	"cogs.minecraft.minecraft",
	"events.command",
	"cogs.minecraft.hypixel.paintball",
	"commands.ping",
	"cogs.prefix",
	"cogs.minecraft.hypixel.skywars",
	"commands.suggest",
	"cogs.wristspasm"
]

@bot.event
async def on_ready():
	time = datetime.datetime.now().strftime("%A, %b %d, %Y - %m/%d/%Y - %I:%M:%S %p")
	status_log_channel = bot.get_channel(core.config.status_log_channel)
	print(f"Connection with Discord established at {time}")
	await bot.change_presence(activity = discord.Game(name = "/help | /suggest"))
	await status_log_channel.send(f"Logged in at {time}.")

if __name__ == "__main__":
	for extension in extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			exception = '{}: {}'.format(type(e).__name__, e)
			print("Failed to load extension {}\n{}".format(extension, exception))

bot.run(core.config.token)

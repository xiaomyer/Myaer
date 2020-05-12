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

import asyncio
from core.config import Config
import datetime
import discord
from discord.ext import commands
import json

async def get_prefix(bot, message):
    return commands.when_mentioned_or("/", "myaer ", "Myaer ")(bot, message)

bot = commands.Bot(
    command_prefix = get_prefix,
    owner_id = 368780147563823114
)

extensions = [
    "jishaku",
    "cogs.minecraft.hypixel.bedwars"
]

config = Config()

@bot.event
async def on_ready():
    time = datetime.datetime.now().strftime("%A, %b %d, %Y - %m/%d/%Y - %I:%M:%S %p")
    global status_log_channel
    status_log_channel = bot.get_channel(config.status_log_channel)
    print(f"Connection with Discord established at {time}")
    await status_log_channel.send(f"Logged in at {time}.")

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exception = '{}: {}'.format(type(e).__name__, e)
            print("Failed to load extension {}\n{}".format(extension, exception))

bot.run(config.token)

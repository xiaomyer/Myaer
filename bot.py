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
import logging
import sys
import traceback

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

async def get_prefix(bot, message):
    return commands.when_mentioned_or("/", "myaer ", "Myaer ")(bot, message)

bot = commands.Bot(
    command_prefix = get_prefix,
    owner_id = 368780147563823114
)

extensions = [
    "jishaku",
    "cogs.minecraft.hypixel.bedwars.bedwars",
    "commands.help",
    "cogs.minecraft.hypixel.leaderboards",
    "cogs.minecraft.minecraft",
    "commands.ping"
]

config = Config()

@bot.event
async def on_ready():
    time = datetime.datetime.now().strftime("%A, %b %d, %Y - %m/%d/%Y - %I:%M:%S %p")
    status_log_channel = bot.get_channel(config.status_log_channel)
    print(f"Connection with Discord established at {time}")
    await status_log_channel.send(f"Logged in at {time}.")

@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.CommandNotFound)

    if hasattr(ctx.command, "on_error"):
        return

    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.MaxConcurrencyReached):
        concurrency_embed = discord.Embed(
            name = "Cooldown",
            color = ctx.author.color,
            description = f"{ctx.author.name}, this command is being ratelimited. Try again in a bit."
        )
        await ctx.send(embed = concurrency_embed)

    elif isinstance(error, commands.CommandOnCooldown):
        cooldown_embed = discord.Embed(
            name = "Cooldown",
            color = ctx.author.color,
            description = f"{ctx.author.name}, you are sending commands too fast. Try again in a bit."
        )
        await ctx.send(embed = cooldown_embed)

    elif isinstance(error, commands.MissingRequiredArgument):
        argument_embed = discord.Embed(
            name = "Error",
            color = ctx.author.color,
            description = f"{ctx.author.name}, you forgot to provide an input of some sort."
        )
        await ctx.send(embed = argument_embed)

    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@bot.check
async def blacklist_check(ctx):
    blacklist = json.load(open("/home/myerfire/Myaer/blacklist.json"))
    if ctx.author.id == bot.owner_id:
        return True
    elif ctx.author.id in blacklist["users"]:
        return False
    else:
        return True

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exception = '{}: {}'.format(type(e).__name__, e)
            print("Failed to load extension {}\n{}".format(extension, exception))

bot.run(config.token)

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

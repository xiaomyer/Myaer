from config import Config
from core.hypixel import Hypixel_
from data.data import Data
from core.static import Static
from discord.ext import commands
import asyncio
import discord
import hypixelaPY
import os
import sys
import traceback

config = Config()
data = Data()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"


async def get_prefix(bot, message):
    if isinstance(message.channel, discord.DMChannel) or not message.guild:
        return commands.when_mentioned_or(config.default_prefix, "myaer ", "Myaer ")(bot, message)
    prefix = config.default_prefix or data.guilds.get(message.guild.id).prefix
    return commands.when_mentioned_or(prefix, "myaer ", "Myaer ")(bot, message)


bot = commands.Bot(
    command_prefix=get_prefix,
    owner_id=config.owner,
    allowed_mentions=discord.AllowedMentions(everyone=False),
    intents=discord.Intents.all()
)
bot.static = Static()
bot.config = config
bot.data = data
bot.hypixel = Hypixel_(bot, config.keys.hypixel)
bot.mojang = hypixelaPY.Mojang()

extensions = [os.path.join(dp, f) for dp, dn, fn in os.walk("cogs") for f in fn] + \
             [os.path.join(dp, f) for dp, dn, fn in os.walk("commands") for f in fn] + \
             [os.path.join(dp, f) for dp, dn, fn in os.walk("modules") for f in fn] + \
             [os.path.join(dp, f) for dp, dn, fn in os.walk("events") for f in fn] + \
             ["jishaku"]
for file in extensions[:]:
    if not file.endswith(".py") and file != "jishaku":  # jishaku cog is a special case
        extensions.remove(file)
bot.static.failed_extensions = []

for extension in extensions:
    try:
        bot.load_extension(((extension.replace("/", "."))[:-3]) if extension.endswith(".py") else extension)
        # i. don't. want. to. talk. about. it.
    except Exception as e:
        exception = '{}: {}'.format(type(e).__name__, e)
        print("Failed to load extension {}\n{}".format(extension, exception))
        error_traceback = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        bot.static.failed_extensions.append((extension, error_traceback))


@bot.event
async def on_error(event, *args, **kwargs):
    error = sys.exc_info()
    error_traceback = "".join(traceback.format_exception(error[0], error[1], error[2]))
    print(error_traceback)
    await bot.config.channels.error.send(embed=discord.Embed(
        title="Exception",
        description=f"```{error_traceback}```",
        timestamp=bot.static.time()
    ))


async def start():
    try:
        await bot.start(config.token)
    except KeyboardInterrupt:
        await bot.logout()


async def stop():
    await bot.logout()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(start())
    except KeyboardInterrupt:
        asyncio.get_event_loop().run_until_complete(stop())

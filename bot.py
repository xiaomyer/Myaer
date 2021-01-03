from config import Config
from core.hypixel import Hypixel_
from data.data import Data
from data.objects import Static
from discord.ext import commands
import asyncio
import datetime
import discord
import hypixelaPY
import os
import sys
import traceback

config = Config()
data = Data()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"


async def get_prefix(bot, message):
    if isinstance(message.channel, discord.DMChannel):
        return commands.when_mentioned_or(config.default_prefix, "myaer ", "Myaer ")(bot, message)
    prefix = config.default_prefix
    guild = data.guilds.get(message.guild.id)
    if guild and guild.prefix:
        prefix = guild.prefix
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
failed_extensions = []

for extension in extensions:
    try:
        bot.load_extension(((extension.replace("/", "."))[:-3]) if extension.endswith(".py") else extension)
    except Exception as e:
        exception = '{}: {}'.format(type(e).__name__, e)
        print("Failed to load extension {}\n{}".format(extension, exception))
        error_traceback = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        failed_extensions.append({"extension": extension, "traceback": error_traceback})


@bot.event
async def on_ready():
    bot.config.get_owner(bot)
    bot.config.channels.get(bot)
    ready_time = datetime.datetime.now()
    print(f"Connection with Discord established at {ready_time.strftime(bot.static.STARTUP_TIME_FORMAT)}")
    for failed_extension in failed_extensions:
        await bot.config.channels.error.send(embed=discord.Embed(
            title=f"Failed to load extension {failed_extension['extension']}",
            description=f"```{failed_extension['traceback']}```"
        ))
    await bot.change_presence(activity=discord.Game(name="Major Update Released! Join https://myer.wtf/discord for information."))
    await bot.config.channels.status.send(f"Logged in at {ready_time.strftime(bot.static.STARTUP_TIME_FORMAT)} (took {(ready_time - bot.static.startup_time).total_seconds()} seconds).")


@bot.event
async def on_error(event, *args, **kwargs):
    error = sys.exc_info()
    error_traceback = "".join(traceback.format_exception(error[0], error[1], error[2]))
    print(error_traceback)
    error_embed = discord.Embed(
        title="Exception",
        description=f"```{error_traceback}```"
    )
    error_embed.set_footer(
        text=datetime.datetime.now().strftime(bot.static.STARTUP_TIME_FORMAT)
    )
    await bot.config.channels.error.send(embed=error_embed)


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

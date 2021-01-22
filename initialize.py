from discord.ext import commands
from datetime import datetime
import discord
import humanfriendly
import pytz


class Initialize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.initialize())
        print(bot.static.separator)
        print("Created task for initialization in bot task loop")

    async def initialize(self):
        print(self.bot.static.separator)
        print("Waiting for internal cache")
        await self.bot.wait_until_ready()
        print("Internal cache is ready")
        self.bot.config.get_owner(self.bot)
        print("Getting owner object for bot.config.owner")
        self.bot.config.channels.get(self.bot)
        print("Getting channel objects for bot.config.channels")
        ready_time = datetime.utcnow()
        ready_time_est = pytz.utc.localize(ready_time).astimezone(pytz.timezone("America/New_York"))
        print(f"Connected to Discord at {ready_time_est.strftime('%A, %b %d, %Y - %m/%d/%Y - %I:%M:%S %p')}")
        for extension, error in self.bot.static.failed_extensions:
            await self.bot.config.channels.events.send(embed=discord.Embed(
                title=f"Failed to load extension {extension}",
                description=f"```{error}```"
            ))
        await self.bot.change_presence(activity=discord.Game(name=f"in {len(self.bot.guilds)} guilds"))
        print("Set Discord presence")
        await self.bot.config.channels.status.send(embed=discord.Embed(
            title="Bot Login",
            color=discord.Color.green(),
            timestamp=ready_time
        ).set_footer(
            text=f"Took {humanfriendly.format_timespan(ready_time - self.bot.static.startup_time)}"
        ))
        print("Sent startup embed")


def setup(bot):
    print("Initializing")
    bot.add_cog(Initialize(bot))

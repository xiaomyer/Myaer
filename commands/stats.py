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
import datetime
import humanfriendly
import humanize
import psutil

import discord
from discord.ext import commands

import core.static.static


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", aliases=["info"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def stats(self, ctx):
        process = psutil.Process()
        with process.oneshot():  # tbh idk what this is, thank you jishaku
            # can't be bothered to find psutil documentation either
            memory_info = process.memory_full_info()
        stats_embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"""[Invite]({discord.utils.oauth_url(ctx.bot.client_id, permissions=ctx.bot.admin_permission)})
[Support](https://inv.wtf/myerfire)
"""
        ).set_author(
            name="Stats",
            icon_url=str(ctx.me.avatar_url_as(static_format="png", size=2048))
        ).set_footer(
            text="Made by MyerFire"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Owner**__",
            value=f"{ctx.bot.owner_user.mention} (myer#0001) [{ctx.bot.owner_id}]",
            inline=False
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Uptime**__",
            value=f"{humanfriendly.format_timespan(datetime.datetime.now() - ctx.bot.startup_time)}",
            inline=False
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Physical Memory**__",
            value=f"{humanize.naturalsize(memory_info.rss)}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Virtual Memory**__",
            value=f"{humanize.naturalsize(memory_info.vms)}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Unique Memory**__",
            value=f"{humanize.naturalsize(memory_info.uss)}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Users**__",
            value=f"{len(ctx.bot.users):,d}",
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Guilds**__",
            value=f"{len(ctx.bot.guilds):,d}"
        )
        await ctx.send(embed=stats_embed)


def setup(bot):
    bot.add_cog(Stats(bot))
    print("Reloaded commands.stats")

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
import discord
import humanfriendly
from discord.ext import commands

import core.static


class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guild", aliases=["g", "server"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def guild(self, ctx: commands.Context):
        await ctx.send(embed=discord.Embed(
            color=ctx.guild.owner.color,
            timestamp=ctx.message.created_at
        ).set_author(
            name=f"{ctx.guild.name} ({ctx.guild.id})",
            icon_url=str(ctx.guild.icon_url_as(static_format="png", size=2048))
        ).add_field(
            name=f"__**{core.static.arrow_bullet_point} Owner**__",
            value=f"{ctx.guild.owner.mention} ({ctx.guild.owner.id})"
        ).add_field(
            name=f"__**{core.static.arrow_bullet_point} Creation Date**__",
            value=f"{ctx.guild.created_at.strftime(ctx.bot.CREATION_TIME_FORMAT)} ({humanfriendly.format_timespan(datetime.datetime.now() - ctx.guild.created_at)} ago)",
            inline=False
        ).add_field(
            name=f"__**{core.static.arrow_bullet_point} Channels ({len(await core.static.get_pure_channels(ctx.guild.channels))})**__",
            value=f"({len(ctx.guild.text_channels)} text and {len(ctx.guild.voice_channels)} voice)",
            inline=False
        ).add_field(
            name=f"__**{core.static.arrow_bullet_point} Members**__",
            value=f"{ctx.guild.member_count:,d}",
        ).add_field(
            name=f"__**{core.static.arrow_bullet_point} Emoji**__",
            value=f"{len(ctx.guild.emojis):,d}"
        ).add_field(
            name=f"__**{core.static.arrow_bullet_point} Roles ({(len(ctx.guild.roles) - 1):,d})**__",  # @everyone
            # role doesn't count
            value=f"{await core.static.get_role_mentions_string(await core.static.get_role_mentions(ctx.guild.roles))}",
            inline=False
        ))


def setup(bot):
    bot.add_cog(Guild(bot))
    print("Reloaded commands.guild")
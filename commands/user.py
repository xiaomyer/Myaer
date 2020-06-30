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
import typing
from discord.ext import commands

import core.static.static


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="user", aliases=["member", "u"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def user(self, ctx, *, user: typing.Union[discord.Member, discord.User, str] = None):  # converts to string if
        # not a Member or User to continue code execution as a makeshift error handler
        # this is so that the argument passed is accessible
        if isinstance(user, str):  # if user is a string, it failed both the Member conversion and the User conversion
            no_user_embed = discord.Embed(
                description=f"User \"{user}\" not found"
            )
            await ctx.send(embed=no_user_embed)
            return
        if not user:
            user = ctx.author
            color = ctx.author.color
        else:
            color = user.color  # user variable is actually a Member object with a color attribute
        user_embed = discord.Embed(
            color=color,
            timestamp=ctx.message.created_at
        )
        user_embed.add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Creation Date**__",
            value=f"{user.created_at.strftime(ctx.bot.CREATION_TIME_FORMAT)} ({humanfriendly.format_timespan(datetime.datetime.now() - user.created_at)} ago)"
        )
        user_embed.set_author(
            name=f"{user.name}#{user.discriminator} ({user.id})",
            icon_url=str(user.avatar_url_as(static_format="png", size=2048))
        )
        await ctx.send(embed=user_embed)


def setup(bot):
    bot.add_cog(User(bot))
    print("Reloaded commands.user")
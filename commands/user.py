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
                description=f"User \"{user}\" not found",
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=no_user_embed)
            return
        if not user:
            user = ctx.author
            color = ctx.author.color
            nick = ctx.author.nick
        else:
            color = user.color
            nick = user.nick if isinstance(user, discord.Member) else None
        user_embed = discord.Embed(
            color=color,
            description=user.mention,
            timestamp=ctx.message.created_at
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Account Created**__",
            value=f"{user.created_at.strftime(ctx.bot.CREATION_TIME_FORMAT)} ({humanfriendly.format_timespan(datetime.datetime.now() - user.created_at)} ago)",
            inline=False
        ).set_author(
            name=f"{user.name}#{user.discriminator} ({nick}) [{user.id}]" if nick else f"{user.name}#{user.discriminator} ({user.id})",
            icon_url=str(user.avatar_url_as(static_format="png", size=2048))
        )
        if isinstance(user, discord.Member):
            join_position = sorted(  # lmao what the hell is this
                ctx.guild.members,  # thank you fire very cool idk what this is
                key=lambda m: m.joined_at or m.created_at
            ).index(user) + 1  # assuming +1 because index
            user_embed.add_field(
                name=f"__**{core.static.static.arrow_bullet_point} Joined Guild**__" if user != ctx.guild.owner else f"__**{core.static.static.arrow_bullet_point} Created Guild**__",
                value=f"{user.joined_at.strftime(ctx.bot.CREATION_TIME_FORMAT)} (#{join_position}) [{humanfriendly.format_timespan(datetime.datetime.now() - user.joined_at)} ago]"
                if user != ctx.guild.owner else
                f"{ctx.guild.created_at.strftime(ctx.bot.CREATION_TIME_FORMAT)} ({humanfriendly.format_timespan(datetime.datetime.now() - ctx.guild.created_at)} ago)"
            ).add_field(
                name=f"__**{core.static.static.arrow_bullet_point} Roles ({len(user.roles) - 1})**__",  # @everyone
                # role doesn't count
                value=f"{await core.static.static.get_role_mentions_string(await core.static.static.get_role_mentions(user.roles))}",
                inline=False
            )
        await ctx.send(embed=user_embed)


def setup(bot):
    bot.add_cog(User(bot))
    print("Reloaded commands.user")
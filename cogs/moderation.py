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

import typing

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", aliases=["banish", "gtfo"])
    @commands.guild_only()
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(manage_guild=True)
    async def ban(self, ctx, target: typing.Union[discord.Member, discord.User, str], *,
                  reason: str = "No reason provided"):
        if not await parse_input(ctx, target):
            return
        banned_notice_embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"You have been banned from {ctx.guild.name} by {ctx.author.mention} ({ctx.author.name}#{ctx.author.discriminator}) for the reason \"{reason}\""
        )
        await target.send(embed=banned_notice_embed)
        await ctx.guild.ban(target, reason=reason)
        banned_embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"Banned {target.name}#{target.discriminator}"
        )
        await ctx.send(embed=banned_embed)

    @commands.command(name="kick")
    @commands.guild_only()
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def kick(self, ctx, target: typing.Union[discord.Member, discord.User, str], *,
                   reason: str = "No reason provided"):
        if not await parse_input(ctx, target):
            return
        kicked_notice_embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"You have been kicked from {ctx.guild.name} by {ctx.author.mention} ({ctx.author.name}#{ctx.author.discriminator}) for the reason \"{reason}\""
        )
        await target.send(embed=kicked_notice_embed)
        await ctx.guild.kick(target, reason=reason)
        kicked_embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"Kicked {target.name}#{target.discriminator}"
        )
        await ctx.send(embed=kicked_embed)

    async def cog_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        ctx.error_handled = True
        if isinstance(error, commands.MissingPermissions):
            permission_needed_embed = discord.Embed(
                color=ctx.author.color,
                timestamp=ctx.message.created_at,
                description=f"You need to have the `{', '.join(error.missing_perms)}` permission(s) to {ctx.command.name} members"
            )
            return await ctx.send(embed=permission_needed_embed)
        if isinstance(error, commands.BotMissingPermissions):
            bot_permissions_needed_embed = discord.Embed(
                color=ctx.author.color,
                timestamp=ctx.message.created_at,
                description=f"I am missing the `{', '.join(error.missing_perms)}` permission(s)"
            )
            return await ctx.send(embed=bot_permissions_needed_embed)


async def parse_input(ctx, _input):
    if isinstance(_input, discord.User):
        not_in_guild_embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"{_input.mention} ({_input.name}#{_input.discriminator}) is not in this server"
        )
        return await ctx.send(embed=not_in_guild_embed)
    if isinstance(_input, str):  # if user is a str, it failed both the Member and User conversion
        not_found_embed = discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"\"{_input}\" was not found"
        )
        return await ctx.send(embed=not_found_embed)
    else:
        return True


def setup(bot):
    bot.add_cog(Moderation(bot))
    print("Reloaded cogs.moderation")

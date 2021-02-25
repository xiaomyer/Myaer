"""
MIT License

Copyright (c) 2020 Myer

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

import sys
import traceback

import discord
from discord.ext import commands

import hypixelaPY
import lastfmpy
from core.exceptions import *


class CommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if prefix := ctx.bot.data.guilds.get(ctx.guild.id).prefix:
            prefix = prefix
        else:
            prefix = ctx.bot.config.default_prefix
        error = getattr(error, "original", error)
        if hasattr(ctx.command, "on_error"):
            return
        ignored = (commands.CommandNotFound,
                   commands.CheckFailure
                   )
        lastfm = (
            lastfmpy.RatelimitExceededError,
            lastfmpy.InvalidInputError,
            lastfmpy.APIKeySuspendedError,
            lastfmpy.OperationFailedError,
            lastfmpy.TemporaryError,
            lastfmpy.ServiceOfflineError
        )
        if isinstance(error, ignored):
            return
        if isinstance(error, hypixelaPY.NoPlayerFoundError):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, f"\"{error.input_}\" is not a valid Minecraft account"))
        elif isinstance(error, NoMinecraftUUID):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, f"You are not verified! `{prefix if bool(prefix) else ctx.bot.config.default_prefix}mc verify <ign>`"))
        elif isinstance(error, NoLastFMUsername):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, f"You are not verified! `{prefix if bool(prefix) else ctx.bot.config.default_prefix}fm set <username>`"))
        elif isinstance(error, lastfm):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, error.message))
        elif isinstance(error, NoSpotifyAccount):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, f"You are not logged into Spotify! `{prefix if bool(prefix) else ctx.bot.config.default_prefix}spotify set`")
            )
        elif isinstance(error, NotSpotifyPremium):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, "You do not have Spotify Premium!")
            )
        elif isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, f"{ctx.author.mention}, you are sending commands too fast"))
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, f"{ctx.author.mention}, `{error.param}` is a required "
                                                f"argument that is missing"))
        elif isinstance(error, commands.BadArgument):
            return await ctx.reply(embed=ctx.bot.static.embed(ctx, str(error)))
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, f"You are missing the`{', '.join(error.missing_perms)}` "
                                                f"permission(s)"))
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.reply(embed=ctx.bot.static.embed(ctx, f"I am missing the`{', '.join(error.missing_perms)}` "
                                                                  f"permission(s)"))
        elif isinstance(error, discord.Forbidden):
            return await ctx.author.send(embed=ctx.bot.static.embed(
                ctx,
                f"""I do not have enough permissions in `{ctx.guild.name}`'s {ctx.channel.mention} channel (or the 
                entire server). The base permissions I require are `Read Messages`, `Send Messages`, `Attach Files`, 
                and `Embed Links`. (moderation commands may require more permissions) If you are having trouble with 
                permissions, giving me the `Administrator` permission will solve any and all problems. For more 
                support, join my [Discord Server](https://myer.wtf/discord)"""))

        error_traceback = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        await ctx.reply(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"```{error_traceback}```"
        ).set_author(
            name="Join my Discord server for help",
            url="https://myer.wtf/discord"
        ))

        await ctx.bot.config.channels.events.send(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            title=f"Ignoring exception in command {ctx.command}\n"
                  f"`{ctx.message.content}`",
            description=(f"in guild `{ctx.guild.name} ({ctx.guild.id})`\n"
                         if isinstance(ctx.message.channel, discord.TextChannel) else
                         "in a DM channel\n") + f"invoked by {ctx.author.mention} ({ctx.author}) [{ctx.author.id}]\n"
                                                f"```{error_traceback}```"))
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandError(bot))
    print("Reloaded events.command_error")

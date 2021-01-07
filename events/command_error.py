"""
MIT License

Copyright (c) 2020 myerfire

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

import hypixelaPY
import sys
import traceback

import discord
from discord.ext import commands
from core.exceptions import NoMinecraftUUID


class CommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)

        if hasattr(ctx.command, "on_error"):
            return

        ignored = (commands.CommandNotFound,
                   commands.CheckFailure
                   )
        if isinstance(error, ignored):
            return

        if isinstance(error, hypixelaPY.NoPlayerFoundError):
            return await ctx.send(
                embed=ctx.bot.static.embed(ctx, f"\"{error.input_}\" is not a valid Minecraft account"))
        elif isinstance(error, NoMinecraftUUID):
            return await ctx.send(
                embed=ctx.bot.static.embed(ctx, f"You are not verified! `/mc verify <ign>`"))
        elif isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.send(
                embed=ctx.bot.static.embed(ctx, f"{ctx.author.mention}, you are sending commands too fast"))
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(
                embed=ctx.bot.static.embed(ctx, f"{ctx.author.mention}, `{error.param}` is a required "
                                                f"argument that is missing"))
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(embed=ctx.bot.static.embed(ctx, str(error)))
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(
                embed=ctx.bot.static.embed(ctx, f"You are missing the`{', '.join(error.missing_perms)}` "
                                                f"permission(s)"))
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(embed=ctx.bot.static.embed(ctx, f"I am missing the`{', '.join(error.missing_perms)}` "
                                                                  f"permission(s)"))
        elif isinstance(error, discord.Forbidden):
            return await ctx.send(embed=ctx.bot.static.embed(
                ctx,
                f"""I do not have enough permissions in `{ctx.guild.name}`'s {ctx.channel.mention} channel (or the 
                entire server). The base permissions I require are `Read Messages`, `Send Messages`, `Attach Files`, 
                and `Embed Links`. (moderation commands may require more permissions) If you are having trouble with 
                permissions, giving me the `Administrator` permission will solve any and all problems. For more 
                support, join my [Discord Server](https://myer.wtf/discord)"""))
        await ctx.send(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"**{error.__class__.__name__}**: {error}"
        ).set_author(
            name="Join my Discord server for help",
            url="https://myer.wtf/discord"
        ))

        error_traceback = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        await ctx.bot.config.channels.error.send(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            title=
            f"""Ignoring exception in command {ctx.command}
        ```{ctx.message.content}```""",
            description=f"""{f'in guild `{ctx.guild.name} ({ctx.guild.id})`' if isinstance(ctx.message.channel, discord.TextChannel) else 'in a DM channel'} 
        invoked by {ctx.author.mention} `({ctx.author.name}#{ctx.author.discriminator}) ({ctx.author.id})`
        ```{error_traceback}```"""
        ))
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandError(bot))
    print("Reloaded events.command_error")

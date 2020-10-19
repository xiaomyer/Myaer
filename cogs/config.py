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

import core.config.guilds
import discord
from discord.ext import commands


async def check_modonly(ctx):
    if await ctx.bot.is_owner(ctx.author):
        return True
    config = await core.config.guilds.get_config(ctx.guild.id)
    modonly = config.get("modonly") if config else None
    if not modonly:
        return True
    if not ctx.channel.id in modonly:
        return True
    else:
        return ctx.author.permissions_in(ctx.channel).manage_messages


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_check(check_modonly)

    @commands.group(name="prefix", invoke_without_command=True)
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def prefix(self, ctx: commands.Context):
        config = await core.config.guilds.get_config(ctx.guild.id)
        prefix = config.get("prefix", None) if config else None
        prefix_embed = discord.Embed(
            name="Prefix",
            description=f"This server's current prefix is `{prefix}`" if prefix else f"This server is using the default prefix, `{self.bot.default_prefix}`"
        )
        return await ctx.send(embed=prefix_embed)

    @prefix.command(name="set")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def set_prefix(self, ctx: commands.Context, prefix):
        if prefix == self.bot.default_prefix:
            reset_data = await core.config.guilds.reset_key(ctx.guild.id, "prefix")
            if reset_data:
                reset_embed = discord.Embed(
                    description=f"Reset this server's prefix from `{reset_data['prefix']}` to `{self.bot.default_prefix}`"
                )
                await ctx.send(embed=reset_embed)
            else:
                not_set_embed = discord.Embed(
                    description=f"This server's prefix is already the default, `{self.bot.default_prefix}`"
                )
                return await ctx.send(embed=not_set_embed)
        elif len(prefix) < 10:
            await core.config.guilds.set_key(ctx.guild.id, "prefix", prefix)
            set_embed = discord.Embed(
                name="Set prefix",
                description=f"Set this server's prefix to `{prefix}`"
            )
            return await ctx.send(embed=set_embed)
        else:
            too_long_embed = discord.Embed(
                name="Too long",
                description="Prefixes should not be that long. Try a shorter one"
            )
            return await ctx.send(embed=too_long_embed)

    @prefix.command(name="reset")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def reset_prefix(self, ctx: commands.Context):
        reset_data = await core.config.guilds.reset_key(ctx.guild.id, "prefix")
        if reset_data:
            reset_embed = discord.Embed(
                description=f"Reset this server's prefix from `{reset_data['prefix']}` to `{self.bot.default_prefix}`"
            )
            return await ctx.send(embed=reset_embed)
        else:
            not_set_embed = discord.Embed(
                description=f"This server's prefix is already the default, `{self.bot.default_prefix}`"
            )
            return await ctx.send(embed=not_set_embed)

    @commands.group(name="modonly", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def modonly(self, ctx: commands.Context):
        config = await core.config.guilds.get_config(ctx.guild.id)
        modonly = config.get("modonly", None) if config else None
        return await ctx.send(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"""The modonly channels in this server are {', '.join([f"<#{channel}>" for channel in modonly])}""" if modonly else "There are no modonly channels in this server"
        ))

    @modonly.command(name="set")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def modonly_set(self, ctx: commands.Context, *channels: discord.TextChannel):
        await core.config.guilds.set_key(ctx.guild.id, "modonly", [channel.id for channel in channels])
        return await ctx.send(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"Set the modonly channels in this server to {', '.join([channel.mention for channel in channels])}"
        ))

    @modonly.command(name="reset")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def modonly_reset(self, ctx: commands.Context):
        await core.config.guilds.reset_key(ctx.guild.id, "modonly")
        return await ctx.send(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description="Reset this server's modonly channels"
        ))


def setup(bot):
    bot.add_cog(Config(bot))
    print("Reloaded cogs.config")

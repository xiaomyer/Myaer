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

import discord
from discord.ext import commands


async def check_staffonly(ctx):
    if await ctx.bot.is_owner(ctx.author): return True
    guild = ctx.bot.data.guilds.get(ctx.guild.id)
    if not guild: return True
    elif not guild.staffonly or not ctx.channel.id in guild.staffonly: return True
    else: return ctx.author.permissions_in(ctx.channel).manage_messages


async def check_modonly(ctx):
    if await ctx.bot.is_owner(ctx.author): return True
    guild = ctx.bot.data.guilds.get(ctx.guild.id)
    if not guild: return True
    elif not guild.modonly or not ctx.channel.id in guild.modonly: return True
    else: return ctx.author.permissions_in(ctx.channel).manage_guild


async def check_adminonly(ctx):
    if await ctx.bot.is_owner(ctx.author): return True
    guild = ctx.bot.data.guilds.get(ctx.guild.id)
    if not guild: return True
    elif not guild.adminonly or not ctx.channel.id in guild.adminonly: return True
    else: return ctx.author.permissions_in(ctx.channel).administrator


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_check(check_modonly)
        bot.add_check(check_adminonly)
        bot.add_check(check_staffonly)

    def cog_unload(self):
        self.bot.remove_check(check_modonly)
        self.bot.remove_check(check_adminonly)
        self.bot.remove_check(check_staffonly)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def prefix(self, ctx: commands.Context):
        guild = ctx.bot.data.guilds.get(ctx.guild.id)
        if not guild:
            prefix = None
        else:
            prefix = guild.prefix
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"This server's current prefix is `{prefix}`" if prefix else f"This server is using the default prefix, `{self.bot.config.default_prefix}`"))

    @prefix.command(name="set")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def set_prefix(self, ctx: commands.Context, prefix):
        if prefix == self.bot.config.default_prefix:
            reset = self.bot.data.guilds.delete(ctx.guild.id, "prefix")
            if reset:
                await ctx.send(embed=ctx.bot.static.embed(ctx, f"Reset this server's prefix from `{reset.prefix}` to `{self.bot.config.default_prefix}`"))
            else:
                return await ctx.send(embed=ctx.bot.static.embed(ctx, f"This server's prefix is already the default, `{self.bot.config.default_prefix}`"))
        elif len(prefix) < 10:
            self.bot.data.guilds.set(ctx.guild.id, "prefix", prefix)
            return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Set this server's prefix to `{prefix}`"))
        else:
            return await ctx.send(embed=ctx.bot.static.embed(ctx, "Prefixes should not be that long. Try a shorter one"))

    @prefix.command(name="reset")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def reset_prefix(self, ctx: commands.Context):
        reset = self.bot.data.guilds.delete(ctx.guild.id, "prefix")
        if reset:
            return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Reset this server's prefix from `{reset.prefix}` to `{self.bot.config.default_prefix}`"))
        else:
            return await ctx.send(embed=ctx.bot.static.embed(ctx, f"This server's prefix is already the default, `{self.bot.config.default_prefix}`"))

    @commands.group(name="staffonly", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def staffonly(self, ctx: commands.Context):
        staffonly = ctx.bot.data.guilds.get(ctx.guild.id).staffonly
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"""The staff-only channels in this server are {', '.join([f"<#{channel}>" for channel in staffonly])}""" if staffonly else "There are no staff-only channels in this server"))

    @staffonly.command(name="set")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def staffonly_set(self, ctx: commands.Context, *channels: discord.TextChannel):
        ctx.bot.data.guilds.set(ctx.guild.id, "staffonly", [channel.id for channel in channels])
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Set the staff-only channels in this server to {', '.join([channel.mention for channel in channels])}"))

    @staffonly.command(name="reset")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def staffonly_reset(self, ctx: commands.Context):
        ctx.bot.data.guilds.delete(ctx.guild.id, "staffonly")
        return await ctx.send(embed=ctx.bot.static.embed(ctx, "Reset this server's staff-only channels"))

    @commands.group(name="modonly", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def modonly(self, ctx: commands.Context):
        modonly = ctx.bot.data.guilds.get(ctx.guild.id).modonly
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"""The mod-only channels in this server are {', '.join([f"<#{channel}>" for channel in modonly])}""" if modonly else "There are no mod-only channels in this server"))

    @modonly.command(name="set")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def modonly_set(self, ctx: commands.Context, *channels: discord.TextChannel):
        ctx.bot.data.guilds.set(ctx.guild.id, "modonly", [channel.id for channel in channels])
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Set the mod-only channels in this server to {', '.join([channel.mention for channel in channels])}"))

    @modonly.command(name="reset")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def modonly_reset(self, ctx: commands.Context):
        ctx.bot.data.guilds.delete(ctx.guild.id, "modonly")
        return await ctx.send(embed=ctx.bot.static.embed(ctx, "Reset this server's mod-only channels"))

    @commands.group(name="adminonly", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def adminonly(self, ctx: commands.Context):
        adminonly = ctx.bot.data.guilds.get(ctx.guild.id).adminonly
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"""The admin-only channels in this server are {', '.join([f"<#{channel}>" for channel in adminonly])}""" if adminonly else "There are no admin-only channels in this server"))

    @adminonly.command(name="set")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def adminonly_set(self, ctx: commands.Context, *channels: discord.TextChannel):
        ctx.bot.data.guilds.set(ctx.guild.id, "adminonly", [channel.id for channel in channels])
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Set the admin-only channels in this server to {', '.join([channel.mention for channel in channels])}"))

    @adminonly.command(name="reset")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def adminonly_reset(self, ctx: commands.Context):
        ctx.bot.data.guilds.delete(ctx.guild.id, "adminonly")
        return await ctx.send(embed=ctx.bot.static.embed(ctx, "Reset this server's admin-only channels"))

    @commands.group(name="starboard", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def starboard(self, ctx: commands.Context):
        starboard = ctx.bot.data.guilds.get(ctx.guild.id).starboard
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"The starboard for this server is <#{starboard}>" if starboard else "There is no starboard set for this server"))

    @starboard.command(name="set")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def starboard_set(self, ctx: commands.Context, channel: discord.TextChannel):
        ctx.bot.data.guilds.set(ctx.guild.id, "starboard", channel.id)
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Set the starboard channel to {channel.mention}"))

    @starboard.command(name="reset")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def starboard_reset(self, ctx: commands.Context):
        reset = ctx.bot.data.guilds.delete(ctx.guild.id, "starboard")
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"{f'Removed the starboard of <#{reset}>' if reset else 'There was no starboard set in this server'}"))


def setup(bot):
    bot.add_cog(Config(bot))
    print("Reloaded cogs.config")

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

import discord
from discord.ext import commands


async def check_staffonly(ctx):
    if await ctx.bot.is_owner(ctx.author): return True
    staffonly = ctx.bot.data.guilds.get(ctx.guild.id).staffonly
    if not staffonly or not ctx.channel.id in staffonly:
        return True
    else:
        return ctx.author.permissions_in(ctx.channel).manage_messages


async def check_modonly(ctx):
    if await ctx.bot.is_owner(ctx.author): return True
    modonly = ctx.bot.data.guilds.get(ctx.guild.id).modonly
    if not modonly or not ctx.channel.id in modonly:
        return True
    else:
        return ctx.author.permissions_in(ctx.channel).manage_guild


async def check_adminonly(ctx):
    if await ctx.bot.is_owner(ctx.author): return True
    adminonly = ctx.bot.data.guilds.get(ctx.guild.id).adminonly
    if not adminonly or not ctx.channel.id in adminonly:
        return True
    else:
        return ctx.author.permissions_in(ctx.channel).administrator


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
        prefix = ctx.bot.data.guilds.get(ctx.guild.id).prefix
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"This server's current prefix is `{prefix}`" if prefix else f"This server is using the default prefix, `{self.bot.config.default_prefix}`"))

    @prefix.command(name="set")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def set_prefix(self, ctx: commands.Context, prefix):
        print(ctx.bot.static.separator)
        print(f"Attempting prefix configuration for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}\n"
              f"Input: {prefix}")
        if prefix == self.bot.config.default_prefix:
            reset = self.bot.data.guilds.delete(ctx.guild.id, "prefix")
            if reset:
                print(f"Successfully set prefix\n"
                      f"Prefix was set to default ({ctx.bot.config.default_prefix})\n"
                      f"Prefix: {reset.prefix} (this has been reset)")
                return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                                 f"Reset this server's prefix from `{reset.prefix}` to `{ctx.bot.config.default_prefix}`"))
            else:
                print(f"Failed setting prefix\n"
                      f"Prefix was already default ({ctx.bot.config.default_prefix})")
                return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                                 f"This server's prefix is already the default, `{ctx.bot.config.default_prefix}`"))
        elif len(prefix) < 10:
            self.bot.data.guilds.set(ctx.guild.id, "prefix", prefix)
            print("Successfully set prefix")
            return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Set this server's prefix to `{prefix}`"))
        else:
            print("Failed setting prefix\n"
                  "Prefix was too long")
            return await ctx.send(
                embed=ctx.bot.static.embed(ctx, "Prefixes should not be that long. Try a shorter one"))

    @prefix.command(name="reset")
    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def reset_prefix(self, ctx: commands.Context):
        print(ctx.bot.static.separator)
        print(f"Attempting prefix reset for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}\n")
        reset = self.bot.data.guilds.delete(ctx.guild.id, "prefix")
        if reset:
            print("Successfully reset prefix")
            return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                             f"Reset this server's prefix from `{reset}` to `{ctx.bot.config.default_prefix}`"))
        else:
            print("Failed resetting prefix\n"
                  f"Prefix was already default {ctx.bot.config.default_prefix}")
            return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                             f"This server's prefix is already the default, `{ctx.bot.config.default_prefix}`"))

    @commands.group(name="staffonly", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def staffonly(self, ctx: commands.Context):
        staffonly = ctx.bot.data.guilds.get(ctx.guild.id).staffonly
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"""The staff-only channels in this server are {', '.join([f"<#{channel}>" for channel in staffonly])}""" if staffonly else "There are no staff-only channels in this server"))

    @staffonly.command(name="set")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def staffonly_set(self, ctx: commands.Context, *channels: discord.TextChannel):
        print(ctx.bot.static.separator)
        print(f"Attempting staffonly configuration for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}\n"
              f"Input: {channels}")
        ctx.bot.data.guilds.set(ctx.guild.id, "staffonly", [channel.id for channel in channels])
        print("Successfully set staffonly channels")
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"Set the staff-only channels in this server to {', '.join([channel.mention for channel in channels])}"))

    @staffonly.command(name="reset")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def staffonly_reset(self, ctx: commands.Context):
        print(ctx.bot.static.separator)
        print(f"Attempting staff-only channel reset for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}\n")
        reset = ctx.bot.data.guilds.delete(ctx.guild.id, "staffonly")
        print("Successfully staff-only channels\n"
              f"staff-only: {reset} (this has been reset)" if reset else
              "Failed resetting staff-only channels\n"
              "staff-only channels were not set")
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"Reset this server's staff-only channels" if reset else "No staff-only channels were set"))

    @commands.group(name="modonly", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def modonly(self, ctx: commands.Context):
        modonly = ctx.bot.data.guilds.get(ctx.guild.id).modonly
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"""The mod-only channels in this server are {', '.join([f"<#{channel}>" for channel in modonly])}""" if modonly else "There are no mod-only channels in this server"))

    @modonly.command(name="set")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def modonly_set(self, ctx: commands.Context, *channels: discord.TextChannel):
        print(ctx.bot.static.separator)
        print(f"Attempting mod-only configuration for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}\n"
              f"Input: {channels}")
        ctx.bot.data.guilds.set(ctx.guild.id, "modonly", [channel.id for channel in channels])
        print("Successfully set mod-only channels")
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"Set the mod-only channels in this server to {', '.join([channel.mention for channel in channels])}"))

    @modonly.command(name="reset")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def modonly_reset(self, ctx: commands.Context):
        print(ctx.bot.static.separator)
        print(f"Attempting mod-only channel reset for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}\n")
        reset = ctx.bot.data.guilds.delete(ctx.guild.id, "modonly")
        print("Successfully reset mod-only channels\n"
              f"admin-only: {reset} (this has been reset)" if reset else
              "Failed resetting mod-only channels\n"
              "mod-only channels were not set")
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"Reset this server's mod-only channels" if reset else "No mod-only channels were set"))

    @commands.group(name="adminonly", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def adminonly(self, ctx: commands.Context):
        adminonly = ctx.bot.data.guilds.get(ctx.guild.id).adminonly
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"""The admin-only channels in this server are {', '.join([f"<#{channel}>" for channel in adminonly])}""" if adminonly else "There are no admin-only channels in this server"))

    @adminonly.command(name="set")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def adminonly_set(self, ctx: commands.Context, *channels: discord.TextChannel):
        print(ctx.bot.static.separator)
        print(f"Attempting admin-only configuration for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}\n"
              f"Input: {channels}")
        ctx.bot.data.guilds.set(ctx.guild.id, "adminonly", [channel.id for channel in channels])
        print("Successfully set admin-only channels")
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"Set the admin-only channels in this server to {', '.join([channel.mention for channel in channels])}"))

    @adminonly.command(name="reset")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def adminonly_reset(self, ctx: commands.Context):
        print(ctx.bot.static.separator)
        print(f"Attempting admin-only channel reset for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}\n")
        reset = ctx.bot.data.guilds.delete(ctx.guild.id, "adminonly")
        print("Successfully reset admin-only channels\n"
              f"admin-only: {reset} (this has been reset)" if reset else
              "Failed resetting admin-only channels\n"
              "admin-only channels were not set")
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"Reset this server's admin-only channels" if reset else "No admin-only channels were set"))

    @commands.group(name="starboard", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def starboard(self, ctx: commands.Context):
        starboard = ctx.bot.data.guilds.get(ctx.guild.id).starboard
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"The starboard for this server is <#{starboard}>" if starboard else "There is no starboard set for this server"))

    @starboard.command(name="set")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def starboard_set(self, ctx: commands.Context, channel: discord.TextChannel):
        print(ctx.bot.static.separator)
        print(f"Attempting starboard set for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}\n"
              f"Input: {channel}")
        ctx.bot.data.guilds.set(ctx.guild.id, "starboard", channel.id)
        print("Successfully set starboard")
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Set the starboard channel to {channel.mention}"))

    @starboard.command(name="reset")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def starboard_reset(self, ctx: commands.Context):
        print(ctx.bot.static.separator)
        print(f"Attempting starboard reset for guild {ctx.guild}\n"
              f"ID: {ctx.guild.id}")
        reset = ctx.bot.data.guilds.delete(ctx.guild.id, "starboard")
        print("Successfully reset starboard\n"
              f"Starboard: {reset} (this has been reset)" if reset else
              "Failed to reset starboard\n"
              "Starboard was not set")
        return await ctx.send(embed=ctx.bot.static.embed(ctx,
                                                         f"{f'Removed the starboard of <#{reset}>' if reset else 'There was no starboard set in this server'}"))


def setup(bot):
    bot.add_cog(Config(bot))
    print("COGS > Reloaded cogs.config")

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


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["mc"], invoke_without_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def minecraft(self, ctx):
        return

    @minecraft.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def verify(self, ctx: commands.Context, query: str):
        print(ctx.bot.static.separator)
        print(f"Attempting Minecraft account verification for user {ctx.author})\n"
              f"ID: {ctx.author.id}\n"
              f"Input: {query}")
        player = await ctx.bot.hypixel.hypixel.player.get(query=query)
        if str(ctx.author) != player.social.discord:
            print(f"Failed Minecraft account verification\n"
                  f"Hypixel Discord name of the given Minecraft account was not the same as the user's discord\n"
                  f"Hypixel Discord name: {player.social.discord}")
            return await ctx.reply(embed=ctx.bot.static.embed(ctx, "Set your Discord name and tag on Hypixel first"))
        print("Successfully verified Minecraft account")
        ctx.bot.data.users.set(ctx.author.id, "minecraft_uuid", player.uuid)
        return await ctx.reply(embed=ctx.bot.static.embed(ctx, f"Verified your Minecraft account as `{player.name}`"))

    @minecraft.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def unverify(self, ctx: commands.Context):
        print(ctx.bot.static.separator)
        print(f"Attempting Minecraft account unverification for user {ctx.author}\n"
              f"ID: {ctx.author.id}")
        reset = ctx.bot.data.users.delete(ctx.author.id, "minecraft_uuid")
        print(f"Unverified Minecraft account\n"
              f"Minecraft UUID: {reset}" if reset else
              f"Failed to unverify Minecraft account\n"
              f"User was not verified")
        return await ctx.reply(embed=ctx.bot.static.embed(ctx,
                                                          f"{'Unverified your Minecraft account' if reset else 'Your Minecraft account was not verified'}"))

    @minecraft.command()
    @commands.is_owner()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def forceverify(self, ctx: commands.Context, user: discord.User, query: str):
        print(ctx.bot.static.separator)
        print(f"Attempting Minecraft account verification for user {user})\n"
              f"ID: {user.id}\n"
              f"Input: {query}")
        player = await ctx.bot.hypixel.hypixel.player.get(query=query)
        print("Successfully verified Minecraft account")
        ctx.bot.data.users.set(user.id, "minecraft_uuid", player.uuid)
        return await ctx.reply(
            embed=ctx.bot.static.embed(ctx, f"Verified {user.mention}'s Minecraft account as `{player.name}`"))

    @minecraft.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def forceunverify(self, ctx: commands.Context, user: discord.User):
        print(ctx.bot.static.separator)
        print(f"Attempting Minecraft account unverification for user {user}\n"
              f"ID: {user.id}")
        reset = ctx.bot.data.users.delete(user.id, "minecraft_uuid")
        print(f"Unverified Minecraft account\n"
              f"Minecraft UUID: {reset.minecraft_uuid} (this has been reset)" if reset else
              f"Failed to unverify Minecraft account\n"
              f"User was not verified")
        return await ctx.reply(embed=ctx.bot.static.embed(ctx,
                                                          f"""{f"Unverified {user.mention}'s Minecraft account" if reset else f"{user.mention}'s Minecraft account was not verified"}"""))


def setup(bot):
    bot.add_cog(Minecraft(bot))
    print("COGS > Reloaded cogs.minecraft.minecraft")

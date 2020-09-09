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

import core.caches.static

import discord
import os

from discord.ext import commands


class ClearCache(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="clearcache", aliases=["cc"], invoke_without_command=True)
    async def clear_cache(self, ctx):
        core.caches.static.friends_cache_db.truncate()
        core.caches.static.friends_cache_db_cache.truncate()
        core.caches.static.leaderboards_cache_db.truncate()
        core.caches.static.leaderboards_cache_db_cache.truncate()
        core.caches.static.players_cache_db.truncate()
        core.caches.static.players_cache_db_cache.truncate()
        await ctx.send(embed=discord.Embed(
            description="Cleared all caches",
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        ))

    @clear_cache.command(name="friends", aliases=["friend"])
    async def clear_cache_friends(self, ctx):
        core.caches.static.friends_cache_db.truncate()
        core.caches.static.friends_cache_db_cache.truncate()
        await ctx.send(embed=discord.Embed(
            description="Cleared friends cache",
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        ))

    @clear_cache.command(name="leaderboards", aliases=["leaderboard"])
    async def clear_cache_leaderboards(self, ctx):
        core.caches.static.leaderboards_cache_db.truncate()
        core.caches.static.leaderboards_cache_db_cache.truncate()
        await ctx.send(embed=discord.Embed(
            description="Cleared leaderboards cache",
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        ))

    @clear_cache.command(name="players", aliases=["player"])
    async def clear_cache_players(self, ctx):
        core.caches.static.players_cache_db.truncate()
        core.caches.static.players_cache_db_cache.truncate()
        await ctx.send(embed=discord.Embed(
            description="Cleared players cache",
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        ))


def setup(bot):
    bot.add_cog(ClearCache(bot))
    print("Reloaded cogs.clear_cache")

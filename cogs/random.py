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

import random

import discord
from discord.ext import commands

import core.static.static


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="random", invoke_without_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def _random(self, ctx):
        await ctx.send(embed=discord.Embed(
            title="Random Commands",
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=f"""```/random member
/random member --channel
/random channel
/random 
```"""
        ))

    @_random.command(name="member")
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def random_member(self, ctx):
        await ctx.send(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=random.choice(ctx.guild.members).mention
        ).set_footer(
            text=f"Chosen out of {ctx.guild.member_count} people"
        ))

    @_random.command(name="channel")
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def channel(self, ctx, *args):
        if bool(len(args)):
            if "--text" in args:
                channels = ctx.guild.text_channels
            elif "--voice" in args:
                channels = ctx.guild.voice_channels
            else:
                channels = await core.static.static.get_pure_channels(ctx.guild.channels)
        else:
            channels = await core.static.static.get_pure_channels(ctx.guild.channels)
        await ctx.send(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=random.choice(channels).mention
        ).set_footer(
            text=f"Chosen out of {len(channels)} channels"
        ))


def setup(bot):
    bot.add_cog(Random(bot))
    print("Reloaded cogs.random")

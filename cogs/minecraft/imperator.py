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


class Imperator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_subcommand=True)
    async def imperator(self, ctx: commands.Context):
        return

    @imperator.command()
    async def player(self, ctx: commands.Context, input_=None):
        player = await ctx.bot.imperator.player.get(ctx=ctx, input_=input_)
        return await ctx.send(embed=discord.Embed(
            color=ctx.author.color,
            title=f"{player.role} {player.name}",
            description=f"Tokens: {player.tokens}\n"
                        f"Kills: {player.kills}\n"
                        f"Deaths: {player.deaths}\n"
                        f"Chunks Travelled: {player.chunks_travelled}"
        ).set_thumbnail(
            url=ctx.bot.static.crafthead.avatar(player.name)
        ))

    @imperator.command()
    async def nation(self, ctx: commands.Context, name):
        nation = await ctx.bot.imperator.imperator.fetch.nation(name=name)
        return await ctx.send(embed=discord.Embed(
            color=nation.color,
            title=nation.formatted,
            description=f"Ideology: {nation.ideology}\n"
                        f"Members: {len(nation.members)}\n"
                        f"Treasury: {nation.bank}"
        ))


def setup(bot):
    bot.add_cog(Imperator(bot))
    print("COGS > Reloaded cogs.minecraft.imperator")

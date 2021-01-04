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

from discord.ext import commands, menus
import discord


class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["lb"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def leaderboards(self, ctx):
        leaderboards = LeaderboardsMenu(ctx)
        await leaderboards.start(ctx)


class LeaderboardsMenu(menus.Menu):
    def __init__(self, ctx_):
        super().__init__(timeout=300.0)
        self.ctx_ = ctx_
        self.index = 0
        self.display = None
        self.loading = discord.Embed(
            color=self.ctx_.author.color,
            description="Loading..."
        )

    def increment_index(self):
        if abs(self.index + 1) > len(self.display) - 1:
            self.index = 0  # loop back
        else:
            self.index += 1

    def decrement_index(self):
        if abs(self.index - 1) > len(self.display) - 1:
            self.index = 0  # loop back
        else:
            self.index -= 1

    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=discord.Embed(
            color=self.ctx.author.color,
            description="React with the game that you want to see the leaderboards for"
        ))

    @menus.button("\u2B05")
    async def on_arrow_backwards(self, payload):
        self.decrement_index()
        return await self.message.edit(embed=self.display[self.index])

    @menus.button("\u23F9")
    async def on_stop(self, payload):
        self.stop()

    @menus.button("\u27A1")
    async def on_arrow_forward(self, payload):
        self.increment_index()
        return await self.message.edit(embed=self.display[self.index])

    @menus.button("<:bedwars:795042441824698398>")
    async def bedwars(self, payload):
        await self.message.edit(embed=self.loading)
        leaderboards = await self.ctx_.bot.hypixel.hypixel.leaderboards.get()
        self.display = (
            await get_bedwars_leaderboard_embed(self.ctx_, leaderboards.bedwars.stars),
            await get_bedwars_leaderboard_embed(self.ctx_, leaderboards.bedwars.finals.overall),
            await get_bedwars_leaderboard_embed(self.ctx_, leaderboards.bedwars.finals.weekly),
            await get_bedwars_leaderboard_embed(self.ctx_, leaderboards.bedwars.wins.overall),
            await get_bedwars_leaderboard_embed(self.ctx_, leaderboards.bedwars.wins.weekly),
        )
        await self.message.edit(embed=self.display[self.index])


async def get_bedwars_leaderboard_embed(ctx, leaderboard):
    players = await ctx.bot.hypixel.leaderboards.get_players(leaderboard)
    players = [get_bedwars_leaderboard_entry_string(ctx, leaderboard, player) for player in players]
    return discord.Embed(
        color=ctx.author.color,
        description="```" + "\n".join(players) + "```"
    ).set_footer(
        text=str(leaderboard)
    )


def get_bedwars_leaderboard_entry_string(ctx, leaderboard, player):
    string = (
        f"[{player.bedwars.prestige.star}{ctx.bot.static.star}] [{player.rank.name}] {player.name}"
        if bool(player.rank) else
        f"[{player.bedwars.prestige.star}{ctx.bot.static.star}] {player.name}")
    if str(leaderboard) == "Overall Wins":
        string = f"{string} - {player.bedwars.wins.wins} wins"
    elif str(leaderboard) == "Overall Final Kills":
        string = f"{string} - {player.bedwars.finals.kills} finals"
    return string


def setup(bot):
    bot.add_cog(Leaderboards(bot))
    print("Reloaded cogs.minecraft.hypixel.leaderboards")

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

from discord.ext import commands, menus
import discord
import math


class Bedwars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["bw"], invoke_without_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def bedwars(self, ctx, input_=None):
        player = await ctx.bot.hypixel.player.get(ctx=ctx, input_=input_)
        stats = (
            self.get_stats_embed(player),
            self.get_stats_embed(player, player.bedwars.solo),
            self.get_stats_embed(player, player.bedwars.doubles),
            self.get_stats_embed(player, player.bedwars.threes),
            self.get_stats_embed(player, player.bedwars.fours),
            self.get_stats_embed(player, player.bedwars.four_v_four)
        )
        fkdr = (
            self.get_fkdr_embed(player),
            self.get_fkdr_embed(player, player.bedwars.solo),
            self.get_fkdr_embed(player, player.bedwars.doubles),
            self.get_fkdr_embed(player, player.bedwars.threes),
            self.get_fkdr_embed(player, player.bedwars.fours),
            self.get_fkdr_embed(player, player.bedwars.four_v_four)
        )
        bblr = (
            self.get_bblr_embed(player),
            self.get_bblr_embed(player, player.bedwars.solo),
            self.get_bblr_embed(player, player.bedwars.doubles),
            self.get_bblr_embed(player, player.bedwars.threes),
            self.get_bblr_embed(player, player.bedwars.fours),
            self.get_bblr_embed(player, player.bedwars.four_v_four)
        )
        wlr = (
            self.get_wlr_embed(player),
            self.get_wlr_embed(player, player.bedwars.solo),
            self.get_wlr_embed(player, player.bedwars.doubles),
            self.get_wlr_embed(player, player.bedwars.threes),
            self.get_wlr_embed(player, player.bedwars.fours),
            self.get_wlr_embed(player, player.bedwars.four_v_four)
        )
        stats = BedwarsMenu(stats, fkdr, bblr, wlr)
        await stats.start(ctx)

    def get_needed_string(self, ratio):
        increase = ratio.increase()
        if increase == float("inf"):
            return f"{increase} needed"
        else:
            return f"{increase:,d} needed"

    def get_stats_embed(self, player, mode=None):
        if not mode:
            mode = player.bedwars  # overall stats
        return discord.Embed(
            color=player.bedwars.prestige.color,
            title=f"[{player.bedwars.prestige.star}{self.bot.static.star}] {player.display}",
            description=f"Winstreak: {mode.winstreak:,d}\n"
                        f"Games Played: {mode.games_played:,d}"
        ).add_field(
            name="Kills",
            value=f"{mode.kills.kills:,d}"
        ).add_field(
            name="Deaths",
            value=f"{mode.kills.deaths:,d}"
        ).add_field(
            name="K/D",
            value=mode.kills.ratio.ratio
        ).add_field(
            name="Final Kills",
            value=f"{mode.finals.kills:,d}"
        ).add_field(
            name="Final Deaths",
            value=f"{mode.finals.deaths:,d}"
        ).add_field(
            name="FK/FD",
            value=mode.finals.ratio.ratio
        ).add_field(
            name="Beds Broken",
            value=f"{mode.beds.broken:,d}"
        ).add_field(
            name="Beds Lost",
            value=f"{mode.beds.lost:,d}"
        ).add_field(
            name="BB/BL",
            value=mode.beds.ratio.ratio
        ).add_field(
            name="Wins",
            value=f"{mode.wins.wins:,d}"
        ).add_field(
            name="Losses",
            value=f"{mode.wins.losses:,d}"
        ).add_field(
            name="W/L",
            value=mode.wins.ratio.ratio
        ).set_footer(
            text=str(mode)
        )

    def get_fkdr_embed(self, player, mode=None):
        if not mode:
            mode = player.bedwars  # overall
        return discord.Embed(
            color=player.bedwars.prestige.color,
            title=f"[{player.bedwars.prestige.star}{self.bot.static.star}] {player.display}",
        ).add_field(
            name="Final Kills",
            value=f"{mode.finals.kills:,d}"
        ).add_field(
            name="Final Deaths",
            value=f"{mode.finals.deaths:,d}"
        ).add_field(
            name="FK/FD",
            value=mode.finals.ratio.ratio
        ).add_field(
            name=f"To {mode.finals.ratio.next} FKDR",
            value=self.get_needed_string(mode.finals.ratio)
        ).set_footer(
            text=f"{mode} FKDR"
        )
    
    def get_wlr_embed(self, player, mode=None):
        if not mode:
            mode = player.bedwars  # overall
        return discord.Embed(
            color=player.bedwars.prestige.color,
            title=f"[{player.bedwars.prestige.star}{self.bot.static.star}] {player.display}",
        ).add_field(
            name="Wins",
            value=f"{mode.wins.wins:,d}"
        ).add_field(
            name="Losses",
            value=f"{mode.wins.losses:,d}"
        ).add_field(
            name="W/L",
            value=mode.wins.ratio.ratio
        ).add_field(
            name=f"To {mode.wins.ratio.next} WLR",
            value=self.get_needed_string(mode.wins.ratio)
        ).set_footer(
            text=f"{mode} WLR"
        )

    def get_bblr_embed(self, player, mode=None):
        if not mode:
            mode = player.bedwars  # overall
        return discord.Embed(
            color=player.bedwars.prestige.color,
            title=f"[{player.bedwars.prestige.star}{self.bot.static.star}] {player.display}",
        ).add_field(
            name="Beds Broken",
            value=f"{mode.beds.broken:,d}"
        ).add_field(
            name="Beds Lost",
            value=f"{mode.beds.lost:,d}"
        ).add_field(
            name="BB/BL",
            value=mode.beds.ratio.ratio
        ).add_field(
            name=f"To {mode.beds.ratio.next} BBLR",
            value=self.get_needed_string(mode.beds.ratio)
        ).set_footer(
            text=f"{mode} BBLR"
        )


class BedwarsMenu(menus.Menu):
    def __init__(self, stats, fkdr, bblr, wlr):
        super().__init__(timeout=300.0)
        self.stats = stats
        self.fkdr = fkdr
        self.bblr = bblr
        self.wlr = wlr
        self.index = 0
        self.display = stats  # default display mode is stats

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
        return await channel.send(embed=self.display[self.index])

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

    @menus.button("<:stats:795017651277135883>")
    async def on_stats(self, payload):
        self.display = self.stats
        return await self.message.edit(embed=self.display[self.index])

    @menus.button("<:fkdr:795014678002663444>")
    async def on_fkdr(self, payload):
        self.display = self.fkdr
        return await self.message.edit(embed=self.display[self.index])

    @menus.button("<:wlr:795017651726450758>")
    async def on_wlr(self, payload):
        self.display = self.wlr
        return await self.message.edit(embed=self.display[self.index])

    @menus.button("<:bblr:795019023065808896>")
    async def on_bblr(self, payload):
        self.display = self.bblr
        return await self.message.edit(embed=self.display[self.index])


def setup(bot):
    bot.add_cog(Bedwars(bot))
    print("Reloaded cogs.minecraft.hypixel.bedwars")

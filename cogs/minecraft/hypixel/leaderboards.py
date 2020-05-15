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

import asyncio
from core.minecraft.hypixel.player.bedwars import Bedwars
from core.minecraft.hypixel.leaderboards.bedwars import BedwarsLeaderboards
import core.characters
from discord.ext import commands
import discord
import core.discord.markdown
from core.minecraft.minecraft import Minecraft
import core.minecraft.hypixel.request
import sys
import time
import traceback

class LeaderboardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bedwars = Bedwars()
        self.bedwarsleaderboards  = core.minecraft.hypixel.leaderboards.bedwars.BedwarsLeaderboards()
        self.markdown = core.discord.markdown.Markdown()
        self.minecraft = core.minecraft.minecraft.Minecraft()
        self.request = core.minecraft.hypixel.request.Request()

    @commands.group(name = "leaderboards", aliases = ["lb", "leaderboard"])
    async def leaderboards(self, ctx):
        return

    @leaderboards.command(name = "bw")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def get_level_leaderboard(self, ctx, *stat):
        if "level" in stat or not stat:
            await ctx.send("Loading level leaderboard...")
            index = 0
            leaderboard = []
            level_leaderboard_embed = discord.Embed(
                name = "Levels leaderboard"
            )
            await self.request.send_leaderboard_request()
            for player in await self.bedwarsleaderboards.get_levels():
                await self.request.send_player_request_uuid(player)
                leaderboard.append([await self.bedwars.get_star(player), core.minecraft.hypixel.request.player_json['player']['displayname'], await self.bedwars.get_fkdr(player)])
                level_leaderboard_embed.add_field(
                    name = f"#{index + 1}",
                    value = await self.markdown.bold(discord.utils.escape_markdown(f"[{leaderboard[index][0]}{core.characters.bedwars_star}] {leaderboard[index][1]}")),
                    inline = False
                )
                index += 1
                print(leaderboard)

            await ctx.send(embed = level_leaderboard_embed)
        elif "level" not in stat:
            await ctx.send("[debug] stat != level")

    @get_level_leaderboard.error
    async def get_level_leaderboard_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                name = "Cooldown"
            )
            cooldown_embed.add_field(
                name = "Cooldown",
                value = "Leaderboard commands have a cooldown of 60s."
            )
            await ctx.send(embed = cooldown_embed)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
def setup(bot):
    bot.add_cog(LeaderboardCommands(bot))
    print("Reloaded cogs.minecraft.hypixel.leaderboards")

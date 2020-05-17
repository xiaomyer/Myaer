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
import core.static
from discord.ext import commands
import discord
import core.discord.markdown
from core.minecraft.minecraft import Minecraft
import core.minecraft.hypixel.request
import sys
import time
import traceback

accuracy_disclaimer = "Weekly leaderboard information is not guranteed to be 100% accurate as the Hypixel API is quite odd."

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
    async def bedwars(self, ctx, *args):
        try:
            leaderboard_type = args[0]
            try:
                leaderboard_time = args[1]
            except IndexError:
                leaderboard_time = None
        except IndexError:
            leaderboard_type = None
        if (leaderboard_type == "level" or leaderboard_type == "star" or leaderboard_type == "levels") or not leaderboard_type:
            loading_embed = discord.Embed(
                name = "Loading",
                description = "Loading Bedwars level leaderboard..."
            )
            message = await ctx.send(embed = loading_embed)
            level_leaderboard_embed = discord.Embed(
                name = "Levels leaderboard"
            )
            index = 0
            leaderboard = []
            await self.request.send_leaderboard_request()
            for player in await self.bedwarsleaderboards.get_levels():
                    await self.request.send_player_request_uuid(player)
                    leaderboard.append([await self.bedwars.get_star(player), core.minecraft.hypixel.request.player_json['player']['displayname'], await self.bedwars.get_fkdr(player)])
                    level_leaderboard_embed.add_field(
                        name = f"#{index + 1}",
                        value = f"{await self.markdown.bold(discord.utils.escape_markdown(f'[{leaderboard[index][0]}{core.static.bedwars_star}] {leaderboard[index][1]}'))} - {leaderboard[index][2]} FKDR",
                        inline = False
                    )
                    index += 1
                    print(leaderboard)

            await message.edit(embed = level_leaderboard_embed)

        elif leaderboard_type == "wins":
            if leaderboard_time == "overall" or not leaderboard_time:
                loading_embed = discord.Embed(
                            name = "Loading",
                            description = "Loading overall Bedwars wins leaderboard..."
                        )
                message = await ctx.send(embed = loading_embed)
                overall_wins_leaderboard_embed = discord.Embed(
                    name = "Levels leaderboard"
                )
                index = 0
                leaderboard = []
                await self.request.send_leaderboard_request()
                for player in await self.bedwarsleaderboards.get_wins():
                    await self.request.send_player_request_uuid(player)
                    leaderboard.append([await self.bedwars.get_star(player), core.minecraft.hypixel.request.player_json['player']['displayname'], await self.bedwars.get_wins(player)])
                    overall_wins_leaderboard_embed.add_field(
                        name = f"#{index + 1}",
                        value = f"{await self.markdown.bold(discord.utils.escape_markdown(f'[{leaderboard[index][0]}{core.static.bedwars_star}] {leaderboard[index][1]}'))} - {leaderboard[index][2]} wins",
                        inline = False
                    )
                    index += 1
                    print(leaderboard)

                await message.edit(embed = overall_wins_leaderboard_embed)

            elif leaderboard_time == "weekly":
                loading_embed = discord.Embed(
                    name = "Loading",
                    description = "Loading weekly Bedwars wins leaderboard..."
                )
                message = await ctx.send(embed = loading_embed)
                weekly_wins_leaderboard_embed = discord.Embed(
                    name = "Levels leaderboard"
                )
                index = 0
                leaderboard = []
                await self.request.send_leaderboard_request()
                for player in await self.bedwarsleaderboards.get_weekly_wins():
                    await self.request.send_player_request_uuid(player)
                    leaderboard.append([await self.bedwars.get_star(player), core.minecraft.hypixel.request.player_json['player']['displayname'], await self.bedwars.get_wins(player)])
                    weekly_wins_leaderboard_embed.add_field(
                        name = f"#{index + 1}",
                        value = f"{await self.markdown.bold(discord.utils.escape_markdown(f'[{leaderboard[index][0]}{core.static.bedwars_star}] {leaderboard[index][1]}'))} - {leaderboard[index][2]} wins",
                        inline = False
                    )
                    index += 1
                    print(leaderboard)
                weekly_wins_leaderboard_embed.set_footer(
                    text = accuracy_disclaimer
                )

                await message.edit(embed = weekly_wins_leaderboard_embed)
        elif (leaderboard_type == "finals" or leaderboard_type == "final"):
            if leaderboard_time == "overall" or not leaderboard_time:
                loading_embed = discord.Embed(
                    name = "Loading",
                    description = "Loading overall Bedwars final kills leaderboard..."
                )
                message = await ctx.send(embed = loading_embed)
                overall_finals_leaderboard_embed = discord.Embed(
                    name = "Levels leaderboard"
                )
                index = 0
                leaderboard = []
                await self.request.send_leaderboard_request()
                for player in await self.bedwarsleaderboards.get_finals():
                    await self.request.send_player_request_uuid(player)
                    leaderboard.append([await self.bedwars.get_star(player), core.minecraft.hypixel.request.player_json['player']['displayname'], await self.bedwars.get_final_kills(player)])
                    overall_finals_leaderboard_embed.add_field(
                        name = f"#{index + 1}",
                        value = f"{await self.markdown.bold(discord.utils.escape_markdown(f'[{leaderboard[index][0]}{core.static.bedwars_star}] {leaderboard[index][1]}'))} - {leaderboard[index][2]} finals",
                        inline = False
                    )
                    index += 1
                    print(leaderboard)

                await message.edit(embed = overall_finals_leaderboard_embed)
            elif leaderboard_time == "weekly":
                loading_embed = discord.Embed(
                    name = "Loading",
                    description = "Loading weekly Bedwars final kills leaderboard..."
                )
                message = await ctx.send(embed = loading_embed)
                weekly_finals_leaderboard_embed = discord.Embed(
                    name = "Levels leaderboard"
                )
                index = 0
                leaderboard = []
                await self.request.send_leaderboard_request()
                for player in await self.bedwarsleaderboards.get_weekly_finals():
                    await self.request.send_player_request_uuid(player)
                    leaderboard.append([await self.bedwars.get_star(player), core.minecraft.hypixel.request.player_json['player']['displayname'], await self.bedwars.get_final_kills(player)])
                    weekly_finals_leaderboard_embed.add_field(
                        name = f"#{index + 1}",
                        value = f"{await self.markdown.bold(discord.utils.escape_markdown(f'[{leaderboard[index][0]}{core.static.bedwars_star}] {leaderboard[index][1]}'))} - {leaderboard[index][2]} finals",
                        inline = False
                    )
                    index += 1
                    print(leaderboard)
                weekly_finals_leaderboard_embed.set_footer(
                    text = accuracy_disclaimer
                )

                await message.edit(embed = weekly_wins_leaderboard_embed)

    @bedwars.error
    async def bedwars_leaderboards_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                name = "Cooldown",
                color = ctx.author.color,
                description = "Leaderboard commands have a cooldown of 60s."
            )
            await ctx.send(embed = cooldown_embed)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(LeaderboardCommands(bot))
    print("Reloaded cogs.minecraft.hypixel.leaderboards")

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

stats_needed_disclaimer = "Note - The amount needed for stat increase assumes that no negative stats are taken (no final deaths, no losses, etc)"

import asyncio
from core.minecraft.hypixel.player.bedwars import Bedwars
import core.static
from discord.ext import commands
import discord
import core.discord.markdown
import core.minecraft.hypixel.request
from core.minecraft.request import MojangAPI

class BedwarsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bedwars = Bedwars()
        self.hypixel = core.minecraft.hypixel.request.HypixelAPI()
        self.mojang = MojangAPI()
        self.markdown = core.discord.markdown.Markdown()

    @commands.command(name = "bw", aliases = ["bwstats"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def get_general_stats(self, ctx, player):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Loading {await self.mojang.get_profile(player)}\'s Bedwars stats..."
            )
            message = await ctx.send(embed = loading_embed)
            await self.hypixel.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel.request
            player_stats_embed = discord.Embed(
                title = await self.markdown.italic((await self.markdown.bold(f"{discord.utils.escape_markdown((await self.mojang.get_profile(player))['name'])}\'s Bedwars Stats"))),
                color = int((await self.bedwars.get_prestige_data(player))['prestige_color'], 16) # 16 - Hex value.
            )
            player_stats_embed.set_thumbnail(
                url = core.static.hypixel_game_icons['Bedwars']
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Level"))),
                value = f"{await self.bedwars.get_star(player)} {core.static.bedwars_star} ({(await self.bedwars.get_prestige_data(player))['prestige']} Prestige)",
                inline = False
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Final Kills"))),
                value = f"{await self.bedwars.get_final_kills(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Final Deaths"))),
                value = f"{await self.bedwars.get_final_deaths(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} FKDR"))),
                value = f"{await self.bedwars.get_fkdr(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Beds Broken"))),
                value = f"{await self.bedwars.get_beds_broken(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Beds Lost"))),
                value = f"{await self.bedwars.get_beds_lost(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} BBLR"))),
                value = f"{await self.bedwars.get_bblr(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Wins"))),
                value = f"{await self.bedwars.get_wins(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Losses"))),
                value = f"{await self.bedwars.get_losses(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} WLR"))),
                value = f"{await self.bedwars.get_wlr(player)}"
            )
            await message.edit(embed = player_stats_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await message.edit(embed = nameerror_embed)

    @commands.command(name = "fkdr")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def get_fkdr_data(self, ctx, player):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Loading {await self.mojang.get_profile(player)}\'s Bedwars FKDR data..."
            )
            message = await ctx.send(embed = loading_embed)
            await self.hypixel.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel.request
            player_fkdr_embed = discord.Embed(
                title = await self.markdown.underline((await self.markdown.bold(f"{(await self.mojang.get_profile(player))['name']}\'s FKDR"))),
                color = int((await self.bedwars.get_prestige_data(player))['prestige_color'], 16) # 16 - Hex value.
            )
            player_fkdr_embed.set_thumbnail(
                url = core.static.hypixel_game_icons['Bedwars']
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} FKDR"))),
                value = f"{await self.bedwars.get_fkdr(player)}"
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Final Kills"))),
                value = f"{await self.bedwars.get_final_kills(player)}"
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Final Deaths"))),
                value = f"{await self.bedwars.get_final_deaths(player)}"
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +1 FKDR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_final_kills(player)), (await self.bedwars.get_final_deaths(player)), 1)} needed",
                inline = False
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +2 FKDR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_final_kills(player)), (await self.bedwars.get_final_deaths(player)), 2)} needed"
            )
            player_fkdr_embed.set_footer(
                text = stats_needed_disclaimer
            )
            await message.edit(embed = player_fkdr_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await message.edit(embed = nameerror_embed)

    @commands.command(name = "bblr")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def get_bblr_data(self, ctx, player):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Loading {await self.mojang.get_profile(player)}\'s Bedwars BBLR data..."
            )
            message = await ctx.send(embed = loading_embed)
            await self.hypixel.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel.request
            player_bblr_embed = discord.Embed(
                title = await self.markdown.underline((await self.markdown.bold(f"{(await self.mojang.get_profile(player))['name']}\'s BBLR"))),
                color = int((await self.bedwars.get_prestige_data(player))['prestige_color'], 16) # 16 - Hex value.
            )
            player_bblr_embed.set_thumbnail(
                url = core.static.hypixel_game_icons['Bedwars']
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} BBLR"))),
                value = f"{await self.bedwars.get_bblr(player)}"
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Beds Broken"))),
                value = f"{await self.bedwars.get_beds_broken(player)}"
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Beds Lost"))),
                value = f"{await self.bedwars.get_beds_lost(player)}"
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +1 BBLR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_beds_broken(player)), (await self.bedwars.get_beds_lost(player)), 1)} needed",
                inline = False
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +2 BBLR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_beds_broken(player)), (await self.bedwars.get_beds_lost(player)), 2)} needed"
            )
            player_bblr_embed.set_footer(
                text = stats_needed_disclaimer
            )
            await message.edit(embed = player_bblr_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await message.edit(embed = nameerror_embed)

    @commands.command(name = "wlr")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def get_wlr_data(self, ctx, player):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Loading {await self.mojang.get_profile(player)}\'s Bedwars WLR data..."
            )
            message = await ctx.send(embed = loading_embed)
            await self.hypixel.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel.request
            player_wlr_embed = discord.Embed(
                title = await self.markdown.underline((await self.markdown.bold(f"{(await self.mojang.get_profile(player))['name']}\'s WLR"))),
                color = int((await self.bedwars.get_prestige_data(player))['prestige_color'], 16) # 16 - Hex value.
            )
            player_wlr_embed.set_thumbnail(
                url = core.static.hypixel_game_icons['Bedwars']
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} WLR"))),
                value = f"{await self.bedwars.get_wlr(player)}"
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Wins"))),
                value = f"{await self.bedwars.get_wins(player)}"
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Losses"))),
                value = f"{await self.bedwars.get_losses(player)}"
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +1 WLR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_wins(player)), (await self.bedwars.get_losses(player)), 1)} needed",
                inline = False
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +2 WLR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_wins(player)), (await self.bedwars.get_losses(player)), 2)} needed"
            )
            player_wlr_embed.set_footer(
                text = stats_needed_disclaimer
            )
            await message.edit(embed = player_wlr_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await message.edit(embed = nameerror_embed)

def setup(bot):
    bot.add_cog(BedwarsCommands(bot))
    print("Reloaded cogs.minecraft.hypixel.bedwars.bedwars")

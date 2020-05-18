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

from core.minecraft.hypixel.player.bedwars import Bedwars
import core.static
from discord.ext import commands
import discord
from core.discord.markdown import Markdown
import core.minecraft.hypixel.request
from core.minecraft.request import MojangAPI

class BedwarsStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bedwars = Bedwars()
        self.hypixel = core.minecraft.hypixel.request.HypixelAPI()
        self.mojang = MojangAPI()
        self.markdown = Markdown()

    @commands.group(name = "bw", invoke_without_command = True)
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def bedwars(self, ctx, player):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Loading {(await self.mojang.get_profile(player))['name']}\'s Bedwars stats..."
            )
            message = await ctx.send(embed = loading_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            message = None
        if message:
            await self.hypixel.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel.request
            player_stats_embed = discord.Embed(
                title = (await self.markdown.bold(f"{discord.utils.escape_markdown((await self.mojang.get_profile(player))['name'])}\'s Bedwars Stats")),
                color = int((await self.bedwars.get_prestige_data())['prestige_color'], 16) # 16 - Hex value.
            )
            player_stats_embed.set_thumbnail(
                url = core.static.hypixel_game_icons['Bedwars']
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Level"))),
                value = f"{await self.bedwars.get_star()} {core.static.bedwars_star} ({(await self.bedwars.get_prestige_data())['prestige']} Prestige)",
                inline = False
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Final Kills"))),
                value = f"{await self.bedwars.get_final_kills()}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Final Deaths"))),
                value = f"{await self.bedwars.get_final_deaths()}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} FKDR"))),
                value = f"{await self.bedwars.get_ratio((await self.bedwars.get_final_kills()), ((await self.bedwars.get_final_deaths())))}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Beds Broken"))),
                value = f"{await self.bedwars.get_beds_broken()}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Beds Lost"))),
                value = f"{await self.bedwars.get_beds_lost()}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} BBLR"))),
                value = f"{await self.bedwars.get_ratio((await self.bedwars.get_beds_broken()), ((await self.bedwars.get_beds_lost())))}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Wins"))),
                value = f"{await self.bedwars.get_wins()}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Losses"))),
                value = f"{await self.bedwars.get_losses()}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} WLR"))),
                value = f"{await self.bedwars.get_ratio((await self.bedwars.get_wins()), ((await self.bedwars.get_losses())))}"
            )
            await message.edit(embed = player_stats_embed)

    @bedwars.command(name = "fkdr")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def get_fkdr_data(self, ctx, player):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Loading {(await self.mojang.get_profile(player))['name']}\'s Bedwars FKDR data..."
            )
            message = await ctx.send(embed = loading_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            message = None
        if message:
            await self.hypixel.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel.request
            player_fkdr_embed = discord.Embed(
                title = await self.markdown.underline((await self.markdown.bold(f"{(await self.mojang.get_profile(player))['name']}\'s FKDR"))),
                color = int((await self.bedwars.get_prestige_data())['prestige_color'], 16) # 16 - Hex value.
            )
            player_fkdr_embed.set_thumbnail(
                url = core.static.hypixel_game_icons['Bedwars']
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} FKDR"))),
                value = f"{await self.bedwars.get_ratio((await self.bedwars.get_final_kills()), ((await self.bedwars.get_final_deaths())))}"
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Final Kills"))),
                value = f"{await self.bedwars.get_final_kills()}"
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Final Deaths"))),
                value = f"{await self.bedwars.get_final_deaths()}"
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +1 FKDR"))),
                value = f"{await self.bedwars.get_increase_stat((await self.bedwars.get_final_kills()), (await self.bedwars.get_final_deaths()), 1)} needed",
                inline = False
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +2 FKDR"))),
                value = f"{await self.bedwars.get_increase_stat((await self.bedwars.get_final_kills()), (await self.bedwars.get_final_deaths()), 2)} needed"
            )
            player_fkdr_embed.set_footer(
                text = core.static.stats_needed_disclaimer
            )
            await message.edit(embed = player_fkdr_embed)

    @bedwars.command(name = "bblr")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def get_bblr_data(self, ctx, player):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Loading {(await self.mojang.get_profile(player))['name']}\'s Bedwars BBLR data..."
            )
            message = await ctx.send(embed = loading_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            message = None
        if message:
            await self.hypixel.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel.request
            player_bblr_embed = discord.Embed(
                title = await self.markdown.underline((await self.markdown.bold(f"{(await self.mojang.get_profile(player))['name']}\'s BBLR"))),
                color = int((await self.bedwars.get_prestige_data())['prestige_color'], 16) # 16 - Hex value.
            )
            player_bblr_embed.set_thumbnail(
                url = core.static.hypixel_game_icons['Bedwars']
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} BBLR"))),
                value = f"{await self.bedwars.get_ratio((await self.bedwars.get_beds_broken()), ((await self.bedwars.get_beds_lost())))}"
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Beds Broken"))),
                value = f"{await self.bedwars.get_beds_broken()}"
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Beds Lost"))),
                value = f"{await self.bedwars.get_beds_lost()}"
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +1 BBLR"))),
                value = f"{await self.bedwars.get_increase_stat((await self.bedwars.get_beds_broken()), (await self.bedwars.get_beds_lost()), 1)} needed",
                inline = False
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +2 BBLR"))),
                value = f"{await self.bedwars.get_increase_stat((await self.bedwars.get_beds_broken()), (await self.bedwars.get_beds_lost()), 2)} needed"
            )
            player_bblr_embed.set_footer(
                text = core.static.stats_needed_disclaimer
            )
            await message.edit(embed = player_bblr_embed)

    @bedwars.command(name = "wlr")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def get_wlr_data(self, ctx, player):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Loading {(await self.mojang.get_profile(player))['name']}\'s Bedwars WLR data..."
            )
            message = await ctx.send(embed = loading_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            message = None
        if message:
            await self.hypixel.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel.request
            player_wlr_embed = discord.Embed(
                title = await self.markdown.underline((await self.markdown.bold(f"{(await self.mojang.get_profile(player))['name']}\'s WLR"))),
                color = int((await self.bedwars.get_prestige_data())['prestige_color'], 16) # 16 - Hex value.
            )
            player_wlr_embed.set_thumbnail(
                url = core.static.hypixel_game_icons['Bedwars']
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} WLR"))),
                value = f"{await self.bedwars.get_ratio((await self.bedwars.get_wins()), ((await self.bedwars.get_losses())))}"
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Wins"))),
                value = f"{await self.bedwars.get_wins()}"
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Losses"))),
                value = f"{await self.bedwars.get_losses()}"
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +1 WLR"))),
                value = f"{await self.bedwars.get_increase_stat((await self.bedwars.get_wins()), (await self.bedwars.get_losses()), 1)} needed",
                inline = False
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} +2 WLR"))),
                value = f"{await self.bedwars.get_increase_stat((await self.bedwars.get_wins()), (await self.bedwars.get_losses()), 2)} needed"
            )
            player_wlr_embed.set_footer(
                text = core.static.stats_needed_disclaimer
            )
            await message.edit(embed = player_wlr_embed)

def setup(bot):
    bot.add_cog(BedwarsStats(bot))
    print("Reloaded cogs.minecraft.hypixel.bedwars.bedwars")

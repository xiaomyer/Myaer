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
import core.characters
from discord.ext import commands
import discord
from core.minecraft.hypixel.hypixel import Hypixel
import core.discord.markdown
import core.minecraft.hypixel.request
from core.minecraft.minecraft import Minecraft

class BedwarsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bedwars = Bedwars()
        self.hypixel = Hypixel()
        self.minecraft = Minecraft()
        self.markdown = core.discord.markdown.Markdown()
        self.request = core.minecraft.hypixel.request.Request()

    @commands.command(name = "bw", aliases = ["bwstats"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def get_general_stats(self, ctx, player):
        try:
            await self.request.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel
            player_stats_embed = discord.Embed(
                title = await self.markdown.italic((await self.markdown.bold(f"{discord.utils.escape_markdown((await self.minecraft.get_profile(player))['name'])}\'s Bedwars Stats"))),
                color = int((await self.bedwars.get_prestige_data(player))['prestige_color'], 16) # 16 - Hex value.
            )
            player_stats_embed.set_thumbnail(
                url = core.minecraft.hypixel.hypixel.icons['Bedwars']
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Level"))),
                value = f"{await self.bedwars.get_star(player)} {core.characters.bedwars_star} ({(await self.bedwars.get_prestige_data(player))['prestige']} Prestige)",
                inline = False
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Final Kills"))),
                value = f"{await self.bedwars.get_final_kills(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Final Deaths"))),
                value = f"{await self.bedwars.get_final_deaths(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} FKDR"))),
                value = f"{await self.bedwars.get_fkdr(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Beds Broken"))),
                value = f"{await self.bedwars.get_beds_broken(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Beds Lost"))),
                value = f"{await self.bedwars.get_beds_lost(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} BBLR"))),
                value = f"{await self.bedwars.get_bblr(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Wins"))),
                value = f"{await self.bedwars.get_wins(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Losses"))),
                value = f"{await self.bedwars.get_losses(player)}"
            )
            player_stats_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} WLR"))),
                value = f"{await self.bedwars.get_wlr(player)}"
            )
            await ctx.send(embed = player_stats_embed)
        except NameError:
            await ctx.send(f"\"{player}\" is not a valid username or UUID.")

    @commands.command(name = "fkdr")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def get_fkdr_data(self, ctx, player):
        try:
            await self.request.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel
            player_fkdr_embed = discord.Embed(
                title = await self.markdown.underline((await self.markdown.bold(f"{(await self.minecraft.get_profile(player))['name']}\'s FKDR"))),
                color = int((await self.bedwars.get_prestige_data(player))['prestige_color'], 16) # 16 - Hex value.
            )
            player_fkdr_embed.set_thumbnail(
                url = core.minecraft.hypixel.hypixel.icons['Bedwars']
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} FKDR"))),
                value = f"{await self.bedwars.get_fkdr(player)}"
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Final Kills"))),
                value = f"{await self.bedwars.get_final_kills(player)}"
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Final Deaths"))),
                value = f"{await self.bedwars.get_final_deaths(player)}"
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} +1 FKDR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_final_kills(player)), (await self.bedwars.get_final_deaths(player)), 1)} needed",
                inline = False
            )
            player_fkdr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} +2 FKDR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_final_kills(player)), (await self.bedwars.get_final_deaths(player)), 2)} needed"
            )
            player_fkdr_embed.set_footer(
                text = stats_needed_disclaimer
            )
            await ctx.send(embed = player_fkdr_embed)
        except NameError:
            await ctx.send(f"Player \"{player}\" does not exist!")

    @commands.command(name = "bblr")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def get_bblr_data(self, ctx, player):
        try:
            await self.request.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel
            player_bblr_embed = discord.Embed(
                title = await self.markdown.underline((await self.markdown.bold(f"{(await self.minecraft.get_profile(player))['name']}\'s BBLR"))),
                color = int((await self.bedwars.get_prestige_data(player))['prestige_color'], 16) # 16 - Hex value.
            )
            player_bblr_embed.set_thumbnail(
                url = core.minecraft.hypixel.hypixel.icons['Bedwars']
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} BBLR"))),
                value = f"{await self.bedwars.get_bblr(player)}"
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Beds Broken"))),
                value = f"{await self.bedwars.get_beds_broken(player)}"
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Beds Lost"))),
                value = f"{await self.bedwars.get_beds_lost(player)}"
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} +1 BBLR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_beds_broken(player)), (await self.bedwars.get_beds_lost(player)), 1)} needed",
                inline = False
            )
            player_bblr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} +2 BBLR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_beds_broken(player)), (await self.bedwars.get_beds_lost(player)), 2)} needed"
            )
            player_bblr_embed.set_footer(
                text = stats_needed_disclaimer
            )
            await ctx.send(embed = player_bblr_embed)
        except NameError:
            await ctx.send(f"Player \"{player}\" does not exist!")

    @commands.command(name = "wlr")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def get_wlr_data(self, ctx, player):
        try:
            await self.request.send_player_request(player) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel
            player_wlr_embed = discord.Embed(
                title = await self.markdown.underline((await self.markdown.bold(f"{(await self.minecraft.get_profile(player))['name']}\'s WLR"))),
                color = int((await self.bedwars.get_prestige_data(player))['prestige_color'], 16) # 16 - Hex value.
            )
            player_wlr_embed.set_thumbnail(
                url = core.minecraft.hypixel.hypixel.icons['Bedwars']
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} WLR"))),
                value = f"{await self.bedwars.get_wlr(player)}"
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Wins"))),
                value = f"{await self.bedwars.get_wins(player)}"
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} Losses"))),
                value = f"{await self.bedwars.get_losses(player)}"
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} +1 WLR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_wins(player)), (await self.bedwars.get_losses(player)), 1)} needed",
                inline = False
            )
            player_wlr_embed.add_field(
                name = await self.markdown.underline((await self.markdown.bold(f"{core.characters.arrow_bullet_point} +2 WLR"))),
                value = f"{await self.bedwars.get_increase_stat(player, (await self.bedwars.get_wins(player)), (await self.bedwars.get_losses(player)), 2)} needed"
            )
            player_wlr_embed.set_footer(
                text = stats_needed_disclaimer
            )
            await ctx.send(embed = player_wlr_embed)
        except NameError:
            await ctx.send(f"Player \"{player}\" does not exist!")

def setup(bot):
    bot.add_cog(BedwarsCommands(bot))
    print("Reloaded cogs.minecraft.hypixel.bedwars.bedwars")

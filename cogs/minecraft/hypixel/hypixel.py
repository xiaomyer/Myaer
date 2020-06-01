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

import core.static
from discord.ext import commands
import discord
import math
from core.minecraft.request import MojangAPI
from core.minecraft.hypixel.player import Player
from core.minecraft.hypixel.static import HypixelStatic
from core.minecraft.verification.verification import Verification

class Hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hypixel_static = HypixelStatic()
        self.mojang = MojangAPI()
        self.player = Player()
        self.verification = Verification()

    @commands.group(name = "hypixel", aliases = ["hp"], invoke_without_command = True)
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def hypixel(self, ctx, *args):
        if len(args):
            try:
                player_data = await self.verification.parse_input(ctx, args[0])
            except AttributeError:
                member_not_verified = discord.Embed(
                    name = "Member not verified",
                    description = f"{args[0]} is not verified. Tell them to do `/mc verify <their-minecraft-ign>`"
                )
                member_not_verified.set_footer(
                    text = "... with Myaer."
                )
                await ctx.send(embed = member_not_verified)
                return
            except NameError:
                nameerror_embed = discord.Embed(
                    name = "Invalid input",
                    description = f"\"{args[0]}\" is not a valid username or UUID."
                )
                await ctx.send(embed = nameerror_embed)
                return
        else: # If no arguments
            try:
                player_data = await self.verification.database_lookup(ctx.author.id)
            except AttributeError:
                unverified_embed = discord.Embed(
                    name = "Not verified",
                    description = "You have to verify with `/mc verify <minecraft-ign>` first."
                )
                await ctx.send(embed = unverified_embed)
                return
        loading_embed = discord.Embed(
            name = "Loading",
            description = f"Loading {player_data['player_formatted_name']}'s Hypixel stats..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_json = await self.player.get_player(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        if (player_json["rank_data"]["rank"]):
            player_info_embed = discord.Embed(
                name = "Player info",
                title = f"[{player_json['rank_data']['rank']}] {player_data['player_formatted_name']}",
                color = int((player_json["rank_data"])["color"], 16) # 16 - hex value
            )
        else:
            player_info_embed = discord.Embed(
                name = "Player info",
                title = f"{player_data['player_formatted_name']}",
                color = int((player_json["rank_data"])["color"], 16) # 16 - hex value
            )
        player_info_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Level**__",
            value = f"{player_json['level_data']['level']} ({player_json['level_data']['percentage']}% to {math.trunc((player_json['level_data']['level']) + 1)})"
        )
        await message.edit(embed = player_info_embed)

def setup(bot):
    bot.add_cog(Hypixel(bot))
    print("Reloaded cogs.minecraft.hypixel")

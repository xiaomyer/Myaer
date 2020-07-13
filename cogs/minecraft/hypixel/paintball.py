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

import math

import discord
from discord.ext import commands

import core.minecraft.hypixel.static.static
import core.minecraft.static
import core.static.static


class Paintball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="paintball", aliases=["pb"], invoke_without_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def paintball(self, ctx, *args):
        player_info = await core.minecraft.static.hypixel_name_handler(ctx, args)
        if player_info:
            player_data = player_info["player_data"]
            player_json = player_info["player_json"]
        else:
            return
        player_stats_embed = discord.Embed(
            title=f"""**{discord.utils.escape_markdown(f"[{player_json['rank_data']['rank']}] {player_data['player_formatted_name']}" if player_json["rank_data"]["rank"] else player_data["player_formatted_name"])}'s Paintball Stats**""",
            color=int(player_json["rank_data"]["color"], 16)  # 16 - hex value
        ).set_thumbnail(
            url=core.minecraft.hypixel.static.static.hypixel_icons["Classic"]
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Coins**__",
            value=f"{(player_json['paintball']['coins']):,d}",
            inline=False
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Kills**__",
            value=f"{(player_json['paintball']['kills']):,d}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Deaths**__",
            value=f"{(player_json['paintball']['deaths']):,d}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} KDR**__",
            value=f"{(await core.minecraft.hypixel.static.static.get_ratio((player_json['paintball']['kills']), (player_json['paintball']['deaths'])))}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Wins**__",
            value=f"{(player_json['paintball']['wins']):,d}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Shots Fired**__",
            value=f"{(player_json['paintball']['shots_fired']):,d}"
        )
        await ctx.send(embed=player_stats_embed)

    @paintball.command(name="kdr")
    async def kdr(self, ctx, *args):
        player_info = await core.minecraft.static.hypixel_name_handler(ctx, args)
        if player_info:
            player_data = player_info["player_data"]
            player_json = player_info["player_json"]
        else:
            return
        player_kdr_embed = discord.Embed(
            title=f"""**{discord.utils.escape_markdown(f"[{player_json['rank_data']['rank']}] {player_data['player_formatted_name']}" if player_json["rank_data"]["rank"] else player_data["player_formatted_name"])}'s Paintball KDR**""",
            color=int(player_json["rank_data"]["color"], 16)  # 16 - Hex value.
        ).set_thumbnail(
            url=core.minecraft.hypixel.static.static.hypixel_icons["Classic"]
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} KDR**__",
            value=f"{await core.minecraft.hypixel.static.static.get_ratio((player_json['paintball']['kills']), ((player_json['paintball']['deaths'])))}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Kills**__",
            value=f"{(player_json['paintball']['kills']):,d}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Deaths**__",
            value=f"{(player_json['paintball']['deaths']):,d}"
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Next 1 KDR**__",
            value=f"{await core.minecraft.hypixel.static.static.get_increase_stat((player_json['paintball']['kills']), (player_json['paintball']['deaths']), ((math.trunc(await core.minecraft.hypixel.static.static.get_ratio((player_json['paintball']['kills']), ((player_json['paintball']['deaths'])))) + 1) - (await core.minecraft.hypixel.static.static.get_ratio(player_json['paintball']['kills'], player_json['paintball']['deaths']))))} needed"
            # don't ask, cause i don't know either; this is for the next integer value
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} +1 KDR**__",
            value=f"{await core.minecraft.hypixel.static.static.get_increase_stat((player_json['paintball']['kills']), (player_json['paintball']['deaths']), 1)} needed",
            inline=False
        ).add_field(
            name=f"__**{core.static.static.arrow_bullet_point} +2 KDR**__",
            value=f"{await core.minecraft.hypixel.static.static.get_increase_stat((player_json['paintball']['kills']), (player_json['paintball']['deaths']), 2)} needed"
        ).set_footer(
            text=core.static.static.stats_needed_disclaimer
        )
        await ctx.send(embed=player_kdr_embed)


def setup(bot):
    bot.add_cog(Paintball(bot))
    print("Reloaded cogs.minecraft.hypixel.paintball")

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
import datetime
import discord
import humanfriendly
import math
from core.paginators import MinecraftHypixelFriends
import core.static.static
import core.minecraft.static
import core.minecraft.hypixel.static.static
import core.minecraft.hypixel.status


class Hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="hypixel", aliases=["hp"], invoke_without_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def hypixel(self, ctx, *args):
        player_info = await core.minecraft.static.hypixel_name_handler(ctx, args, get_guild=True, get_status=True)
        if player_info:
            player_data = player_info["player_data"]
            player_json = player_info["player_json"]
        else:
            return
        player_info_embed = discord.Embed(
            title=f"""**{discord.utils.escape_markdown(f"[{player_json['rank_data']['rank']}] {player_data['player_formatted_name']}" if player_json["rank_data"]["rank"] else player_data["player_formatted_name"])}**""",
            color=int((player_json["rank_data"])["color"], 16)  # 16 - hex value
        )
        player_info_embed.set_thumbnail(
            url=core.minecraft.hypixel.static.static.hypixel_icons["Main"]
        )
        player_info_embed.set_footer(
            text="Session data may not be 100% accurate as the data is cached. Use /session for 100% accurate data",
            icon_url=f"{self.bot.mc_heads_api}avatar/{player_data['minecraft_uuid']}/100"
        )
        player_info_embed.add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Level**__",
            value=f"{player_json['level_data']['level']} ({player_json['level_data']['percentage']}% to {math.trunc((player_json['level_data']['level']) + 1)})"
        )
        player_info_embed.add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Karma**__",
            value=f"{(player_json['karma']):,d}"
        )
        player_info_embed.add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Achievement Points**__",
            value=f"{(player_json['achievement_points']):,d}"
        )
        player_info_embed.add_field(
            name=f"__**{core.static.static.arrow_bullet_point} First Login**__",
            value=f"{datetime.date.fromtimestamp((player_json['login_times']['first']) / 1000)}"
        )
        player_info_embed.add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Last Login**__",
            value=
            f"""{datetime.date.fromtimestamp((player_json['login_times']['last']) / 1000)}
({(humanfriendly.format_timespan(((datetime.datetime.now()) - (datetime.datetime.fromtimestamp((player_json['login_times']['last']) / 1000))), max_units=2))} ago)
[{player_json["status"]["session"]["formatted"] if player_json["status"]["online"] else "currently offline"}]"""
        )
        if player_json["guild_data"]:  # checks if player is in a guild
            player_info_embed.add_field(
                name=f"__**{core.static.static.arrow_bullet_point} Guild**__",
                value=f"""{discord.utils.escape_markdown(f"{player_json['guild_data']['name']} [{player_json['guild_data']['tag']}]" if player_json["guild_data"]["tag"] else f"{player_json['guild_data']['name']}")}""",
                # checks if player's guild has a tag
                inline=False
            )
        await ctx.send(embed=player_info_embed)

    @commands.command(name="friends")
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def friends(self, ctx, *args):
        await ctx.trigger_typing()
        loading_embed = discord.Embed(
            description="The friends list command may take a very long time depending on whether or not cached data is available. If you end up reading this message, please be patient"
        )
        message = await ctx.send(embed=loading_embed)
        player_info = await core.minecraft.static.hypixel_name_handler(ctx, args, get_friends=True)
        if player_info:
            player_data = player_info["player_data"]
            player_json = player_info["player_json"]
        else:
            return
        friends_string = []
        for friend in player_json["friends"]:
            friends_string.append(
                f"""{discord.utils.escape_markdown(f"[{str(friend['rank_data']['rank'])}] {str(friend['name'])}" if (friend["rank_data"]["rank"]) else (str(friend["name"])))} - on {datetime.date.fromtimestamp((friend["friended_at"]) / 1000)}""")
        friends_paginator = menus.MenuPages(source=MinecraftHypixelFriends(friends_string, player_json),
                                            clear_reactions_after=True)
        await message.delete()
        await friends_paginator.start(ctx)

    @commands.command(name="status", aliases=["session"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def status(self, ctx, *args):
        player_info = await core.minecraft.static.hypixel_name_handler(ctx, args, use_cache=False, get_status=True)
        if player_info:
            player_data = player_info["player_data"]
            player_json = player_info["player_json"]
        else:
            return
        player_status_embed = discord.Embed(
            description=f"""**{discord.utils.escape_markdown(f"[{player_json['rank_data']['rank']}] {player_data['player_formatted_name']}" if player_json["rank_data"]["rank"] else player_data["player_formatted_name"])}** is {player_json["status"]["session"]["formatted"] if player_json["status"]["online"] else "currently offline"}""",
            color=int((player_json["rank_data"])["color"], 16)  # 16 - hex value
        )
        await ctx.send(embed=player_status_embed)

    @hypixel.command(name="guild", aliases=["g"], invoke_without_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def guild(self, ctx, *args):
        player_info = await core.minecraft.static.hypixel_name_handler(ctx, args)
        if player_info:
            player_data = player_info["player_data"]
            player_json = player_info["player_json"]
        else:
            return
        try:
            guild_json = await core.minecraft.hypixel.guild.get_guild_data(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name="Invalid input",
                description=f"{player_data['player_formatted_name']} is not in a guild"
            )
            return
        player_guild_embed = discord.Embed(
            name="Player guild",
            title=f"""{discord.utils.escape_markdown(f"{guild_json['name']} [{guild_json['tag']}]") if guild_json["tag"] else f"{guild_json['name']}"}""",
            color=int((guild_json['color']), 16) if guild_json['color'] else ctx.author.color
        )
        player_guild_embed.add_field(
            name=f"__**{core.static.static.arrow_bullet_point} Level**__",
            value=f"{guild_json['level_data']['level']} ({guild_json['level_data']['percentage']}% to {math.trunc((guild_json['level_data']['level'])) + 1})"
        )
        await ctx.send(embed=player_guild_embed)

    @hypixel.command(name="cleargames", aliases=["cg"])
    @commands.is_owner()
    async def clear_games_cache(self, ctx):
        await core.minecraft.hypixel.status.clear_games_cache()
        cleared_game_cache_embed = discord.Embed(
            description="Cleared the `games` variable cache from `core/minecraft/hypixel/status.py`"
        )
        await ctx.send(embed=cleared_game_cache_embed)


def setup(bot):
    bot.add_cog(Hypixel(bot))
    print("Reloaded cogs.minecraft.hypixel.hypixel")

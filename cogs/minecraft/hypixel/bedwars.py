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
from discord.ext import commands
import discord
import core.minecraft.hypixel.request
import core.static
from core.minecraft.request import MojangAPI
from core.minecraft.verification.verification import Verification

class BedwarsStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bedwars = Bedwars()
        self.hypixel = core.minecraft.hypixel.request.HypixelAPI()
        self.mojang = MojangAPI()
        self.user_converter = commands.UserConverter()
        self.verification = Verification()

    @commands.group(name = "bw", invoke_without_command = True)
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def bedwars(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s Bedwars stats..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_stats_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Bedwars Stats**",
            color = int((await self.bedwars.get_prestige_data(player_stats['star']))["prestige_color"], 16) # 16 - Hex value.
        )
        player_stats_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Level**__",
            value = f"{player_stats['star']} {core.static.bedwars_star} ({(await self.bedwars.get_prestige_data(player_stats['star']))['prestige']} Prestige)",
            inline = False
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['final_kills']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['final_deaths']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['final_kills']), ((player_stats['final_deaths'])))}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['beds_broken']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['beds_lost']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['beds_broken']), ((player_stats['beds_lost'])))}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['wins']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['losses']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['wins']), ((player_stats['losses'])))}"
        )
        await message.edit(embed = player_stats_embed)

    @bedwars.command(name = "stats") # Safety net in case the player"s name is "solo" or "doubles"
    async def bedwars_stats(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s Bedwars stats..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_stats_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Bedwars Stats**",
            color = int((await self.bedwars.get_prestige_data(player_stats['star']))["prestige_color"], 16) # 16 - Hex value.
        )
        player_stats_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Level**__",
            value = f"{player_stats['star']} {core.static.bedwars_star} ({(await self.bedwars.get_prestige_data(player_stats['star']))['prestige']} Prestige)",
            inline = False
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['final_kills']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['final_deaths']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['final_kills']), ((player_stats['final_deaths'])))}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['beds_broken']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['beds_lost']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['beds_broken']), ((player_stats['beds_lost'])))}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['wins']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['losses']}"
        )
        player_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['wins']), ((player_stats['losses'])))}"
        )
        await message.edit(embed = player_stats_embed)

    @bedwars.command(name = "solo", aliases = ["1", "solos"])
    async def solo_bedwars(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s Solo Bedwars stats..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_solo_stats_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Solo Bedwars Stats**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_solo_stats_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_solo_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['solo']['final_kills']}"
        )
        player_solo_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['solo']['final_deaths']}"
        )
        player_solo_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['solo']['final_kills']), ((player_stats['solo']['final_deaths'])))}"
        )
        player_solo_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['solo']['beds_broken']}"
        )
        player_solo_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['solo']['beds_lost']}"
        )
        player_solo_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['solo']['beds_broken']), ((player_stats['solo']['beds_lost'])))}"
        )
        player_solo_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['solo']['wins']}"
        )
        player_solo_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['solo']['losses']}"
        )
        player_solo_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['solo']['wins']), ((player_stats['solo']['losses'])))}"
        )
        await message.edit(embed = player_solo_stats_embed)

    @bedwars.command(name = "doubles", aliases = ["2", "2s", "double", "twos"])
    async def doubles_bedwars(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s Doubles Bedwars stats..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.send(embed = nameerror_embed)
            return
        player_doubles_stats_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Doubles Bedwars Stats**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_doubles_stats_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_doubles_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['doubles']['final_kills']}"
        )
        player_doubles_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['doubles']['final_deaths']}"
        )
        player_doubles_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['doubles']['final_kills']), ((player_stats['doubles']['final_deaths'])))}"
        )
        player_doubles_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['doubles']['beds_broken']}"
        )
        player_doubles_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['doubles']['beds_lost']}"
        )
        player_doubles_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['doubles']['beds_broken']), ((player_stats['doubles']['beds_lost'])))}"
        )
        player_doubles_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['doubles']['wins']}"
        )
        player_doubles_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['doubles']['losses']}"
        )
        player_doubles_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['doubles']['wins']), ((player_stats['doubles']['losses'])))}"
        )
        await message.edit(embed = player_doubles_stats_embed)

    @bedwars.command(name = "threes", aliases = ["3", "3s", "triple", "three"])
    async def threes_bedwars(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s Threes Bedwars stats..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_threes_stats_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Threes Bedwars Stats**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_threes_stats_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_threes_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['threes']['final_kills']}"
        )
        player_threes_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['threes']['final_deaths']}"
        )
        player_threes_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['threes']['final_kills']), ((player_stats['threes']['final_deaths'])))}"
        )
        player_threes_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['threes']['beds_broken']}"
        )
        player_threes_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['threes']['beds_lost']}"
        )
        player_threes_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['threes']['beds_broken']), ((player_stats['threes']['beds_lost'])))}"
        )
        player_threes_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['threes']['wins']}"
        )
        player_threes_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['threes']['losses']}"
        )
        player_threes_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['threes']['wins']), ((player_stats['threes']['losses'])))}"
        )
        await message.edit(embed = player_threes_stats_embed)

    @bedwars.command(name = "fours", aliases = ["4", "4s", "four"])
    async def fours_bedwars(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s Fours Bedwars stats..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_fours_stats_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Fours Bedwars Stats**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_fours_stats_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_fours_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['fours']['final_kills']}"
        )
        player_fours_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['fours']['final_deaths']}"
        )
        player_fours_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['fours']['final_kills']), ((player_stats['fours']['final_deaths'])))}"
        )
        player_fours_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['fours']['beds_broken']}"
        )
        player_fours_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['fours']['beds_lost']}"
        )
        player_fours_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['fours']['beds_broken']), ((player_stats['fours']['beds_lost'])))}"
        )
        player_fours_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['fours']['wins']}"
        )
        player_fours_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['fours']['losses']}"
        )
        player_fours_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['fours']['wins']), ((player_stats['fours']['losses'])))}"
        )
        await message.edit(embed = player_fours_stats_embed)

    @bedwars.command(name = "4v4")
    async def four_v_four_bedwars(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s 4v4 Bedwars stats..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_four_v_four_stats_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s 4v4 Bedwars Stats**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_four_v_four_stats_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_four_v_four_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['four_v_four']['final_kills']}"
        )
        player_four_v_four_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['four_v_four']['final_deaths']}"
        )
        player_four_v_four_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['four_v_four']['final_kills']), ((player_stats['four_v_four']['final_deaths'])))}"
        )
        player_four_v_four_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['four_v_four']['beds_broken']}"
        )
        player_four_v_four_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['four_v_four']['beds_lost']}"
        )
        player_four_v_four_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['four_v_four']['beds_broken']), ((player_stats['four_v_four']['beds_lost'])))}"
        )
        player_four_v_four_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['four_v_four']['wins']}"
        )
        player_four_v_four_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['four_v_four']['losses']}"
        )
        player_four_v_four_stats_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['four_v_four']['wins']), ((player_stats['four_v_four']['losses'])))}"
        )
        await message.edit(embed = player_four_v_four_stats_embed)

    @bedwars.group(name = "fkdr", invoke_without_command = True)
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def fkdr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s FKDR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_fkdr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s FKDR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_fkdr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['final_kills']), ((player_stats['final_deaths'])))}"
        )
        player_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['final_kills']}"
        )
        player_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['final_deaths']}"
        )
        player_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['final_kills']), (player_stats['final_deaths']), 1)} needed",
            inline = False
        )
        player_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['final_kills']), (player_stats['final_deaths']), 2)} needed"
        )
        player_fkdr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_fkdr_embed)

    @fkdr.command(name = "solo", aliases = ["1", "solos"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def solo_fkdr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s solo FKDR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_solo_fkdr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Solo FKDR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_solo_fkdr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_solo_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['solo']['final_kills']), ((player_stats['solo']['final_deaths'])))}"
        )
        player_solo_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['solo']['final_kills']}"
        )
        player_solo_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['solo']['final_deaths']}"
        )
        player_solo_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['solo']['final_kills']), (player_stats['solo']['final_deaths']), 1)} needed",
            inline = False
        )
        player_solo_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['solo']['final_kills']), (player_stats['solo']['final_deaths']), 2)} needed"
        )
        player_solo_fkdr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_solo_fkdr_embed)

    @fkdr.command(name = "doubles", aliases = ["2", "2s", "double"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def doubles_fkdr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s doubles FKDR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_doubles_fkdr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Doubles FKDR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_doubles_fkdr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_doubles_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['doubles']['final_kills']), ((player_stats['doubles']['final_deaths'])))}"
        )
        player_doubles_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['doubles']['final_kills']}"
        )
        player_doubles_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['doubles']['final_deaths']}"
        )
        player_doubles_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['doubles']['final_kills']), (player_stats['doubles']['final_deaths']), 1)} needed",
            inline = False
        )
        player_doubles_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['doubles']['final_kills']), (player_stats['doubles']['final_deaths']), 2)} needed"
        )
        player_doubles_fkdr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_doubles_fkdr_embed)

    @fkdr.command(name = "threes", aliases = ["3", "3s", "triple", "three"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def threes_fkdr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s threes FKDR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_threes_fkdr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Threes FKDR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_threes_fkdr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_threes_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['threes']['final_kills']), ((player_stats['threes']['final_deaths'])))}"
        )
        player_threes_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['threes']['final_kills']}"
        )
        player_threes_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['threes']['final_deaths']}"
        )
        player_threes_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['threes']['final_kills']), (player_stats['threes']['final_deaths']), 1)} needed",
            inline = False
        )
        player_threes_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['threes']['final_kills']), (player_stats['threes']['final_deaths']), 2)} needed"
        )
        player_threes_fkdr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_threes_fkdr_embed)

    @fkdr.command(name = "fours", aliases = ["4", "4s", "four"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def fours_fkdr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s fours FKDR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_fours_fkdr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Fours FKDR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_fours_fkdr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_fours_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['fours']['final_kills']), ((player_stats['fours']['final_deaths'])))}"
        )
        player_fours_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['fours']['final_kills']}"
        )
        player_fours_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['fours']['final_deaths']}"
        )
        player_fours_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['fours']['final_kills']), (player_stats['fours']['final_deaths']), 1)} needed",
            inline = False
        )
        player_fours_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['fours']['final_kills']), (player_stats['fours']['final_deaths']), 2)} needed"
        )
        player_fours_fkdr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_fours_fkdr_embed)

    @fkdr.command(name = "4v4")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def four_v_four_fkdr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s 4v4 FKDR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_four_v_four_fkdr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s 4v4 FKDR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_four_v_four_fkdr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_four_v_four_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} FKDR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['four_v_four']['final_kills']), ((player_stats['four_v_four']['final_deaths'])))}"
        )
        player_four_v_four_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Kills**__",
            value = f"{player_stats['four_v_four']['final_kills']}"
        )
        player_four_v_four_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Final Deaths**__",
            value = f"{player_stats['four_v_four']['final_deaths']}"
        )
        player_four_v_four_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['four_v_four']['final_kills']), (player_stats['four_v_four']['final_deaths']), 1)} needed",
            inline = False
        )
        player_four_v_four_fkdr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 FKDR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['four_v_four']['final_kills']), (player_stats['four_v_four']['final_deaths']), 2)} needed"
        )
        player_four_v_four_fkdr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_four_v_four_fkdr_embed)

    @bedwars.group(name = "bblr", invoke_without_command = True)
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def bblr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s BBLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_bblr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s BBLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_bblr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['beds_broken']), ((player_stats['beds_lost'])))}"
        )
        player_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['beds_broken']}"
        )
        player_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['beds_lost']}"
        )
        player_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['beds_broken']), (player_stats['beds_lost']), 1)} needed",
            inline = False
        )
        player_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['beds_broken']), (player_stats['beds_lost']), 2)} needed"
        )
        player_bblr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_bblr_embed)

    @bblr.command(name = "solo", aliases = ["1", "solos"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def solo_bblr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s solo BBLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_solo_bblr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Solo BBLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_solo_bblr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_solo_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['solo']['beds_broken']), ((player_stats['solo']['beds_lost'])))}"
        )
        player_solo_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['solo']['beds_broken']}"
        )
        player_solo_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['solo']['beds_lost']}"
        )
        player_solo_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['solo']['beds_broken']), (player_stats['solo']['beds_lost']), 1)} needed",
            inline = False
        )
        player_solo_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['solo']['beds_broken']), (player_stats['solo']['beds_lost']), 2)} needed"
        )
        player_solo_bblr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_solo_bblr_embed)

    @bblr.command(name = "doubles", aliases = ["2", "2s", "double", "twos"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def doubles_bblr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s doubles BBLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_doubles_bblr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Doubles BBLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_doubles_bblr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_doubles_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['doubles']['beds_broken']), ((player_stats['doubles']['beds_lost'])))}"
        )
        player_doubles_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['doubles']['beds_broken']}"
        )
        player_doubles_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['doubles']['beds_lost']}"
        )
        player_doubles_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['doubles']['beds_broken']), (player_stats['doubles']['beds_lost']), 1)} needed",
            inline = False
        )
        player_doubles_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['doubles']['beds_broken']), (player_stats['doubles']['beds_lost']), 2)} needed"
        )
        player_doubles_bblr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_doubles_bblr_embed)

    @bblr.command(name = "threes", aliases = ["3", "3s", "triple", "three"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def threes_bblr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s threes BBLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_threes_bblr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Threes BBLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_threes_bblr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_threes_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['threes']['beds_broken']), ((player_stats['threes']['beds_lost'])))}"
        )
        player_threes_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['threes']['beds_broken']}"
        )
        player_threes_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['threes']['beds_lost']}"
        )
        player_threes_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['threes']['beds_broken']), (player_stats['threes']['beds_lost']), 1)} needed",
            inline = False
        )
        player_threes_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['threes']['beds_broken']), (player_stats['threes']['beds_lost']), 2)} needed"
        )
        player_threes_bblr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_threes_bblr_embed)

    @bblr.command(name = "fours", aliases = ["4", "4s", "four"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def fours_bblr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s fours BBLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_fours_bblr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Fours BBLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_fours_bblr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_fours_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['fours']['beds_broken']), ((player_stats['fours']['beds_lost'])))}"
        )
        player_fours_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['fours']['beds_broken']}"
        )
        player_fours_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['fours']['beds_lost']}"
        )
        player_fours_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['fours']['beds_broken']), (player_stats['fours']['beds_lost']), 1)} needed",
            inline = False
        )
        player_fours_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['fours']['beds_broken']), (player_stats['fours']['beds_lost']), 2)} needed"
        )
        player_fours_bblr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_fours_bblr_embed)

    @bblr.command(name = "4v4")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def four_v_four_bblr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s 4v4 BBLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_four_v_four_bblr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s 4v4 BBLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_four_v_four_bblr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_four_v_four_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} BBLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['four_v_four']['beds_broken']), ((player_stats['four_v_four']['beds_lost'])))}"
        )
        player_four_v_four_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Broken**__",
            value = f"{player_stats['four_v_four']['beds_broken']}"
        )
        player_four_v_four_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Beds Lost**__",
            value = f"{player_stats['four_v_four']['beds_lost']}"
        )
        player_four_v_four_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['four_v_four']['beds_broken']), (player_stats['four_v_four']['beds_lost']), 1)} needed",
            inline = False
        )
        player_four_v_four_bblr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 BBLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['four_v_four']['beds_broken']), (player_stats['four_v_four']['beds_lost']), 2)} needed"
        )
        player_four_v_four_bblr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_four_v_four_bblr_embed)

    @bedwars.group(name = "wlr", invoke_without_command = True)
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def wlr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s WLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_wlr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s WLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_wlr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['wins']), ((player_stats['losses'])))}"
        )
        player_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['wins']}"
        )
        player_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['losses']}"
        )
        player_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['wins']), (player_stats['losses']), 1)} needed",
            inline = False
        )
        player_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['wins']), (player_stats['losses']), 2)} needed"
        )
        player_wlr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_wlr_embed)

    @wlr.command(name = "solo", aliases = ["1", "solos"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def solo_wlr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s solo WLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_solo_wlr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Solo WLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_solo_wlr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_solo_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['solo']['wins']), ((player_stats['solo']['losses'])))}"
        )
        player_solo_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['solo']['wins']}"
        )
        player_solo_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['solo']['losses']}"
        )
        player_solo_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['solo']['wins']), (player_stats['solo']['losses']), 1)} needed",
            inline = False
        )
        player_solo_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['solo']['wins']), (player_stats['solo']['losses']), 2)} needed"
        )
        player_solo_wlr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_solo_wlr_embed)

    @wlr.command(name = "doubles", aliases = ["2", "2s", "double", "twos"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def doubles_wlr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s doubles WLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_doubles_wlr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Doubles WLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_doubles_wlr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_doubles_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['doubles']['wins']), ((player_stats['doubles']['losses'])))}"
        )
        player_doubles_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['doubles']['wins']}"
        )
        player_doubles_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['doubles']['losses']}"
        )
        player_doubles_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['doubles']['wins']), (player_stats['doubles']['losses']), 1)} needed",
            inline = False
        )
        player_doubles_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['doubles']['wins']), (player_stats['doubles']['losses']), 2)} needed"
        )
        player_doubles_wlr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_doubles_wlr_embed)

    @wlr.command(name = "threes", aliases = ["3", "3s", "triple", "three"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def threes_wlr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s threes WLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_threes_wlr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Threes WLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_threes_wlr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_threes_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['trees']['wins']), ((player_stats['threes']['losses'])))}"
        )
        player_threes_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['trees']['wins']}"
        )
        player_threes_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['threes']['losses']}"
        )
        player_threes_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['trees']['wins']), (player_stats['threes']['losses']), 1)} needed",
            inline = False
        )
        player_threes_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['trees']['wins']), (player_stats['threes']['losses']), 2)} needed"
        )
        player_threes_wlr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_threes_wlr_embed)

    @wlr.command(name = "fours", aliases = ["4", "4s", "four"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def fours_wlr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s fours WLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_fours_wlr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s Fours WLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_fours_wlr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_fours_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['fours']['wins']), ((player_stats['fours']['losses'])))}"
        )
        player_fours_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['fours']['wins']}"
        )
        player_fours_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['fours']['losses']}"
        )
        player_fours_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['fours']['wins']), (player_stats['fours']['losses']), 1)} needed",
            inline = False
        )
        player_fours_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['fours']['wins']), (player_stats['fours']['losses']), 2)} needed"
        )
        player_fours_wlr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_fours_wlr_embed)

    @wlr.command(name = "4v4")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def four_v_four_wlr(self, ctx, *args):
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
            description = f"Loading {player_data['player_formatted_name']}'s 4v4 WLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            player_stats = await self.bedwars.get_stats(player_data["minecraft_uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        player_four_v_four_wlr_embed = discord.Embed(
            title = f"**{discord.utils.escape_markdown(player_data['player_formatted_name'])}'s 4v4 WLR**",
            color = int((await self.bedwars.get_prestige_data(player_stats["star"]))["prestige_color"], 16) # 16 - Hex value.
        )
        player_four_v_four_wlr_embed.set_thumbnail(
            url = core.static.hypixel_game_icons["Bedwars"]
        )
        player_four_v_four_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} WLR**__",
            value = f"{await self.bedwars.get_ratio((player_stats['four_v_four']['wins']), ((player_stats['four_v_four']['losses'])))}"
        )
        player_four_v_four_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Wins**__",
            value = f"{player_stats['four_v_four']['wins']}"
        )
        player_four_v_four_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} Losses**__",
            value = f"{player_stats['four_v_four']['losses']}"
        )
        player_four_v_four_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +1 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['four_v_four']['wins']), (player_stats['four_v_four']['losses']), 1)} needed",
            inline = False
        )
        player_four_v_four_wlr_embed.add_field(
            name = f"__**{core.static.arrow_bullet_point} +2 WLR**__",
            value = f"{await self.bedwars.get_increase_stat((player_stats['four_v_four']['wins']), (player_stats['four_v_four']['losses']), 2)} needed"
        )
        player_four_v_four_wlr_embed.set_footer(
            text = core.static.stats_needed_disclaimer
        )
        await message.edit(embed = player_four_v_four_wlr_embed)
def setup(bot):
    bot.add_cog(BedwarsStats(bot))
    print("Reloaded cogs.minecraft.hypixel.bedwars")

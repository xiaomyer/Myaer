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

import datetime

import discord
from discord.ext import commands, menus

import core.config.users
import core.minecraft.request
import core.minecraft.static
import core.static.static
from core.paginators import MinecraftNameHistory


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="minecraft", aliases=["mc"], invoke_without_command=True)
    async def minecraft(self, ctx):
        minecraft_commands_embed = discord.Embed(
            title="Minecraft Commands",
            description=
            """
            ```/mc history
            /mc uuid
            /mc skin
            /mc verify
            /mc unverify```
            """
        )
        await ctx.send(embed=minecraft_commands_embed)

    @minecraft.command(name="history", aliases=["names", "namehistory"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def name_history(self, ctx, *args):
        player_info = await core.minecraft.static.name_handler(ctx, args)
        if player_info:
            player_data = player_info
        else:
            return
        await ctx.channel.trigger_typing()
        name_history = await core.minecraft.request.get_name_history_uuid(player_data["minecraft_uuid"])
        index = len(name_history) - 1
        name_history_string = []
        for name in name_history:  # the index is only needed because something else has to be done for the first one
            if index == 0:  # First name does not have changedToAt attribute
                name_history_string.append(f"{name_history[index][0]}")
            else:
                name_history_string.append(
                    f"{discord.utils.escape_markdown(name_history[index][0])} - *on {datetime.date.fromtimestamp((name_history[index][1]) / 1000)}*")
            index -= 1
        name_history_paginator = menus.MenuPages(source=MinecraftNameHistory(name_history_string),
                                                 clear_reactions_after=True)
        await name_history_paginator.start(ctx)

    @minecraft.command(name="uuid")
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def uuid(self, ctx, *args):
        player_info = await core.minecraft.static.name_handler(ctx, args)
        if player_info:
            player_data = player_info
        else:
            return
        await ctx.channel.trigger_typing()
        player_uuid_embed = discord.Embed(
            description=f"{player_data['player_formatted_name']}\'s UUID is {player_data['minecraft_uuid']}.",
            color=ctx.author.color
        )
        await ctx.send(embed=player_uuid_embed)

    @minecraft.command(name="skin")
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def skin(self, ctx, *args):
        player_info = await core.minecraft.static.name_handler(ctx, args)
        if player_info:
            player_data = player_info
        else:
            return
        await ctx.channel.trigger_typing()
        player_skin_embed = discord.Embed(
            title=f"**{player_data['player_formatted_name']}'s Minecraft Skin**",
            description=f"[Raw Skin]({self.bot.SURGEPLAY_API}skin/{player_data['minecraft_uuid']})",
            color=ctx.author.color
        )
        player_skin_embed.set_image(
            url=f"{self.bot.SURGEPLAY_API}full/256/{player_data['minecraft_uuid']}",
            # don't ask me what the number is, idk either; i think it's the maximum size for images
        )
        player_skin_embed.set_thumbnail(
            url=f"{self.bot.SURGEPLAY_API}head/64/{player_data['minecraft_uuid']}"
        )
        await ctx.send(embed=player_skin_embed)

    @minecraft.command(name="verify", aliases=["link"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def verify(self, ctx, ign):
        player_info = await core.minecraft.static.hypixel_name_handler_no_database(ctx, ign, use_cache=False)
        if player_info:
            player_data = player_info["player_data"]
            player_json = player_info["player_json"]
        else:
            return
        try:
            await core.config.users.minecraft_verify(ctx.author.id, f"{ctx.author.name}#{ctx.author.discriminator}",
                                                     player_data["minecraft_uuid"],
                                                     player_json["social_media"]["discord"])
            verified_embed = discord.Embed(
                name="Verified Minecraft IGN",
                description=f"Verified your Minecraft account as \"{player_data['player_formatted_name']}\"",
                color=ctx.author.color
            )
            await ctx.send(embed=verified_embed)
        except ValueError:
            already_has_discord_hypixel_embed = discord.Embed(
                name="Already linked on Hypixel",
                description=f"{player_data['player_formatted_name']} has a linked Discord account on Hypixel that is not yours.",
                color=ctx.author.color
            )
            already_has_discord_hypixel_embed.set_footer(
                text="If this is your Minecraft account, update your Discord name on Hypixel.",
            )
            await ctx.send(embed=already_has_discord_hypixel_embed)
            return
        except AttributeError:
            no_discord_hypixel_embed = discord.Embed(
                name="No Discord linked on Hypixel",
                description=f"{player_data['player_formatted_name']} does not have a linked Discord name on Hypixel."
            )
            no_discord_hypixel_embed.set_footer(
                text="Set your Discord name on Hypixel."
            )
            await ctx.send(embed=no_discord_hypixel_embed)
            return

    @minecraft.command(name="forceverify", aliases=["forcelink"])
    @commands.is_owner()
    async def force_verify(self, ctx, target: discord.User, ign):
        try:
            player_data = await core.minecraft.request.get_profile(ign)
        except NameError:
            nameerror_embed = discord.Embed(
                name="Invalid input",
                description=f"\"{ign}\" is not a valid username or UUID."
            )
            await ctx.send(embed=nameerror_embed)
            return
        await core.config.users.minecraft_force_verify(target.id, player_data['uuid'])
        verified_embed = discord.Embed(
            name="Verified Minecraft IGN",
            description=f"Verified {target}\'s Minecraft account as \"{player_data['name']}\"",
            color=ctx.author.color
        )
        await ctx.send(embed=verified_embed)

    @minecraft.command(name="unverify", aliases=["unlink"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def unverify(self, ctx):
        try:
            unverified_data = await core.config.users.reset_key(ctx.author.id, "minecraft_uuid")
            unverified_embed = discord.Embed(
                name="Unverified",
                description=f"Unverified your Minecraft account \"{(await core.minecraft.request.get_profile_uuid((unverified_data['minecraft_uuid'])))['name']}\".",
                color=ctx.author.color
            )
            unverified_embed.set_footer(
                text=f"UUID was {(await core.minecraft.request.get_profile_uuid(unverified_data['minecraft_uuid']))['uuid']}"
            )
            await ctx.send(embed=unverified_embed)
        except NameError:
            not_verified_embed = discord.Embed(
                name="Not verified",
                description="Your Minecraft account was not verified.",
                color=ctx.author.color
            )
            await ctx.send(embed=not_verified_embed)

    @minecraft.command(name="forceunverify", aliases=["forceunlink"])
    @commands.is_owner()
    async def force_unverify(self, ctx, target: discord.Member):
        try:
            unverified_data = await core.config.users.reset_key(target.id, "minecraft_uuid")
            unverified_embed = discord.Embed(
                name="Unverified",
                description=f"Unverified {target}\'s Minecraft account \"{(await core.minecraft.request.get_profile_uuid((unverified_data['minecraft_uuid'])))['name']}\".",
                color=ctx.author.color
            )
            unverified_embed.set_footer(
                text=f"UUID was {(await core.minecraft.request.get_profile_uuid(unverified_data['minecraft_uuid']))['uuid']}"
            )
            await ctx.send(embed=unverified_embed)
        except NameError:
            not_verified_embed = discord.Embed(
                name="Not verified",
                description=f"{target}\'s Minecraft account was not verified.",
                color=ctx.author.color
            )
            await ctx.send(embed=not_verified_embed)


def setup(bot):
    bot.add_cog(Minecraft(bot))
    print("Reloaded cogs.minecraft")

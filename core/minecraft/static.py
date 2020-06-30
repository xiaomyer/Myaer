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

import discord

import core.minecraft.hypixel.player
import core.minecraft.request
import core.minecraft.verification.verification


async def hypixel_name_handler(ctx, args, *, use_cache: bool = True, get_guild: bool = False, get_friends: bool = False,
                               get_status: bool = False):
    player_name = None
    if bool(len(args)):
        try:
            player_data = await core.minecraft.verification.verification.parse_input(ctx, args[0])
            player_uuid = player_data["minecraft_uuid"]
            player_name = player_data["player_formatted_name"]
        except AttributeError:
            member_not_verified = discord.Embed(
                name="Member not verified",
                description=f"{args[0]} is not verified. Tell them to do `/mc verify <their-minecraft-ign>`",
                color=ctx.author.color
            )
            await ctx.send(embed=member_not_verified)
            return
        except NameError:
            nameerror_embed = discord.Embed(
                name="Invalid input",
                description=f"\"{args[0]}\" is not a valid username or UUID",
                color=ctx.author.color
            )
            await ctx.send(embed=nameerror_embed)
            return
    else:
        player_uuid = await core.minecraft.verification.verification.database_lookup_uuid(ctx.author.id)
        if player_uuid is None:
            unverified_embed = discord.Embed(
                name="Not verified",
                description="You have to verify with `/mc verify <minecraft-ign>` first, or specify a player name",
                color=ctx.author.color
            )
            await ctx.send(embed=unverified_embed)
            return
    try:
        player_json = await core.minecraft.hypixel.player.get_player_data(player_uuid, use_cache=use_cache,
                                                                          get_guild=get_guild, get_friends=get_friends,
                                                                          get_status=get_status)
        player_name = player_json["name"] if not player_name else player_name
        player_data = {
            "player_formatted_name": player_name,
            "minecraft_uuid": player_uuid
        }
    except NameError:
        nameerror_embed = discord.Embed(
            name="Invalid input",
            description=f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats",
            color=ctx.author.color
        )
        await ctx.send(embed=nameerror_embed)
        return
    except OverflowError:
        ratelimit_embed = discord.Embed(
            name="Ratelimit met",
            description="API ratelimit has been reached. Please try again later"
        )
        await ctx.send(embed=ratelimit_embed)
        return
    player_info = {
        "player_data": player_data,
        "player_json": player_json
    }
    return player_info


async def hypixel_name_handler_no_database(ctx, player, *, use_cache: bool = True, get_status: bool = False,
                                           get_guild: bool = False, get_friends: bool = False):
    try:
        player_profile = await core.minecraft.request.get_profile(player)
        player_data = {
            "player_formatted_name": player_profile["name"],
            "minecraft_uuid": player_profile["uuid"]
        }
        player_uuid = player_data["minecraft_uuid"]
        player_name = player_data["player_formatted_name"]
    except NameError:
        nameerror_embed = discord.Embed(
            name="Invalid input",
            description=f"\"{player}\" is not a valid username or UUID",
            color=ctx.author.color
        )
        await ctx.send(embed=nameerror_embed)
        return
    try:
        player_json = await core.minecraft.hypixel.player.get_player_data(player_uuid, use_cache=use_cache,
                                                                          get_status=get_status, get_guild=get_guild,
                                                                          get_friends=get_friends)
        player_data = {
            "player_formatted_name": player_name,
            "minecraft_uuid": player_uuid
        }
    except NameError:
        nameerror_embed = discord.Embed(
            name="Invalid input",
            description=f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats",
            color=ctx.author.color
        )
        await ctx.send(embed=nameerror_embed)
        return
    except OverflowError:
        ratelimit_embed = discord.Embed(
            name="Ratelimit met",
            description="API ratelimit has been reached. Please try again later"
        )
        await ctx.send(embed=ratelimit_embed)
        return
    player_info = {
        "player_data": player_data,
        "player_json": player_json
    }
    return player_info


async def name_handler(ctx, args):
    player_name = None
    if bool(len(args)):
        try:
            player_data = await core.minecraft.verification.verification.parse_input(ctx, args[0])
            player_uuid = player_data["minecraft_uuid"]
            player_name = player_data["player_formatted_name"]
        except AttributeError:
            member_not_verified = discord.Embed(
                name="Member not verified",
                description=f"{args[0]} is not verified. Tell them to do `/mc verify <their-minecraft-ign>`",
                color=ctx.author.color
            )
            await ctx.send(embed=member_not_verified)
            return
        except NameError:
            nameerror_embed = discord.Embed(
                name="Invalid input",
                description=f"\"{args[0]}\" is not a valid username or UUID.",
                color=ctx.author.color
            )
            await ctx.send(embed=nameerror_embed)
            return
    else:
        player_data = await core.minecraft.verification.verification.database_lookup(ctx.author.id)
        if player_data is None:
            unverified_embed = discord.Embed(
                name="Not verified",
                description="You have to verify with `/mc verify <minecraft-ign>` first.",
                color=ctx.author.color
            )
            await ctx.send(embed=unverified_embed)
            return
    return player_data

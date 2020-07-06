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

from core.exceptions import NotVerified
import core.config.users
import core.minecraft.hypixel.player
import core.minecraft.request


async def parse_input(ctx, _input):
    try:
        player_discord = await ctx.bot.user_converter.convert(ctx, _input)
    except discord.ext.commands.errors.BadArgument:
        player_discord = None
    try:
        if player_discord and (
                player_discord.mentioned_in(ctx.message) or _input.isdigit()):  # if input is a discord id
            uuid = await database_lookup_uuid(player_discord.id)
            if uuid:
                player_data = {
                    "player_formatted_name": (await core.minecraft.request.get_profile(uuid))["name"],
                    "minecraft_uuid": uuid
                }
                return player_data
            else:
                raise AttributeError
        else:
            try:
                player_info = await core.minecraft.request.get_profile(_input)
                player_data = {
                    "player_formatted_name": player_info["name"],
                    "minecraft_uuid": player_info["uuid"]
                }
                return player_data
            except NameError:
                raise NameError
    except IndexError:
        raise NotVerified


async def database_lookup_uuid(discord_id):
    result = await core.config.users.get_config(discord_id)
    return result.get("minecraft_uuid", None)


async def database_lookup(discord_id):
    uuid = await database_lookup_uuid(discord_id)
    if uuid is None:
        return
    player_data = {
        "player_formatted_name": (await core.minecraft.request.get_profile(uuid))["name"],
        "minecraft_uuid": uuid
    }
    return player_data

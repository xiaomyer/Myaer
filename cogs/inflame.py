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
from discord.ext import commands

import core.config.users
from core.exceptions import HypixelDiscordNotMatching, NoHypixelDiscord
import core.minecraft.request
import core.minecraft.static
import core.static.static

default_message = 730171718353813605


class Inflame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = 730098132527874210
        self.verification_channel = 730104991393513502
        self.guild_member_role = 730099734194290698
        self.awaiting_verification = 730105293060702269
        self.verified_role = 730098132527874217

    async def cog_check(self, ctx):
        if ctx.guild.id == self.guild:
            if ctx.channel.id == self.verification_channel:
                return True
        else:
            return False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == self.guild:
            verification_channel_object = self.bot.get_channel(self.verification_channel)
            await verification_channel_object.purge(limit=100, check=on_member_purge_check)

    @commands.command(name="verify")
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def verify(self, ctx, ign):
        player_info = await core.minecraft.static.hypixel_name_handler_no_database(ctx, ign, use_cache=False,
                                                                                   get_guild=True)
        if player_info:
            player_data = player_info["player_data"]
            player_json = player_info["player_json"]
        else:
            return
        try:
            await core.config.users.minecraft_verify(
                ctx.author.id,
                f"{ctx.author.name}#{ctx.author.discriminator}",
                player_data["minecraft_uuid"],
                player_json["social_media"]["discord"]
            )
            verified_embed = discord.Embed(
                name="Verified Minecraft IGN",
                description=f"Verified you as \"{player_data['player_formatted_name']}\"",
                color=ctx.author.color
            )
            await (await ctx.send(embed=verified_embed)).delete()
            await ctx.message.delete()
        except HypixelDiscordNotMatching:
            already_has_discord_hypixel_embed = discord.Embed(
                timestamp=ctx.message.created_at,
                description=f"{player_data['player_formatted_name']} has a linked Discord account on Hypixel that is not yours.",
                color=ctx.author.color
            )
            already_has_discord_hypixel_embed.set_footer(
                text="If this is your Minecraft account, update your Discord name on Hypixel.",
            )
            await ctx.send(embed=already_has_discord_hypixel_embed)
            return
        except NoHypixelDiscord:
            no_discord_hypixel_embed = discord.Embed(
                name="No Discord linked on Hypixel",
                description=f"{player_data['player_formatted_name']} does not have a linked Discord name on Hypixel."
            )
            no_discord_hypixel_embed.set_footer(
                text="Set your Discord name on Hypixel."
            )
            await ctx.send(embed=no_discord_hypixel_embed)
            return
        verified_role_object = ctx.guild.get_role(self.verified_role)
        await ctx.author.add_roles(verified_role_object)
        awaiting_verification_role_object = ctx.guild.get_role(self.awaiting_verification)
        await ctx.author.remove_roles(awaiting_verification_role_object)
        if player_json["guild"]["name"] == "Inflame":
            guild_member_role_object = ctx.guild.get_role(self.guild_member_role)
            await ctx.author.add_roles(guild_member_role_object)

    @commands.command(name="forceverify")
    @commands.is_owner()
    async def force_verify(self, ctx, target: discord.Member, ign):
        player_info = await core.minecraft.static.hypixel_name_handler_no_database(ctx, ign, use_cache=False,
                                                                                   get_guild=True)
        if player_info:
            player_data = player_info["player_data"]
            player_json = player_info["player_json"]
        else:
            return
        await core.config.users.minecraft_force_verify(target.id, player_data['minecraft_uuid'])
        verified_embed = discord.Embed(
            name="Verified Minecraft IGN",
            description=f"Verified {target} as \"{player_data['player_formatted_name']}\"",
            color=ctx.author.color
        )
        await ctx.send(embed=verified_embed)
        verified_role_object = ctx.guild.get_role(self.verified_role)
        await target.add_roles(verified_role_object)
        awaiting_verification_role_object = ctx.guild.get_role(self.awaiting_verification)
        await target.remove_roles(awaiting_verification_role_object)
        if player_json["guild"]["name"] == "Inflame":
            guild_member_role_object = ctx.guild.get_role(self.guild_member_role)
            await target.add_roles(guild_member_role_object)


def on_member_purge_check(message):
    if message.id == default_message:
        return False
    else:
        return True


def setup(bot):
    bot.add_cog(Inflame(bot))
    print("Reloaded cogs.flamelight")

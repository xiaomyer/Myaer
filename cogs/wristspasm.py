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

from discord.ext import commands
import discord
import core.minecraft.request
from core.minecraft.hypixel.player import Player
import core.minecraft.hypixel.static
import core.static

master = 394984668656566274

admin_role = 633073051784708099

moderator_role = 700177102925987850

trial_moderator_role = 700177445957140521

async def override_check(ctx):
    admin_role_object = ctx.guild.get_role(admin_role)
    moderator_role_object = ctx.guild.get_role(moderator_role)
    trial_moderator_role_object = ctx.guild.get_role(trial_moderator_role)
    if (ctx.author.id == master) or (admin_role_object in ctx.author.roles) or (moderator_role_object in ctx.author.roles) or (trial_moderator_role_object in ctx.author.roles):
        return True
    else:
        return False

class WristSpasm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = 600311056627269642
        self.player = Player()
        self.roles = {
            "Stone" : 600314048617119757,
            "Iron" : 600313179452735498,
            "Gold" : 600313143398236191,
            "Diamond" : 600313179452735498,
            "Emerald" : 600311885971062784,
            "Sapphire" : 601086287285583872,
            "Ruby" : 610930173675831336,
            "Crystal" : 610930335135432879,
            "Opal" : 610929429635661846,
            "Amethyst" : 610929550674886686,
            "Rainbow" : 614848336649912342
        }

    async def cog_check(self, ctx):
        if ctx.guild.id == self.guild:
            return True
        else:
            return False

    @commands.group(name = "wristspasm", aliases = ["spasm"], invoke_without_command = True)
    async def wristspasm(self, ctx):
        await ctx.send("the best guild")

    @wristspasm.command(name = "verify")
    async def prestige_role(self, ctx, player):
        try:
            player_data = await core.minecraft.request.get_profile(player)
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Verifying you as {player_data['name']}..."
            )
            loading_embed.set_footer(
                text = core.static.wrist_spasm_disclaimer
            )
            message = await ctx.send(embed = loading_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            return
        try:
            player_stats = await self.player.get_player(player_data["uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        prestige = (await core.minecraft.hypixel.static.get_bedwars_prestige_data(player_stats["bedwars"]["star"]))["prestige"]
        prestige_role = self.roles[prestige]
        prestige_role_object = ctx.guild.get_role(prestige_role)
        if ctx.author.nick != player_data["name"]:
            try:
                await ctx.author.edit(nick = player_data["name"])
                nickname_changed_embed = discord.Embed(
                    name = "Nickname changed",
                    description = f"Changed your nickname to {player_data['name']}."
                )
                nickname_changed_embed.set_footer(
                    text = core.static.wrist_spasm_disclaimer
                )
                await ctx.send(embed = nickname_changed_embed)
            except discord.errors.Forbidden:
                forbidden_embed = discord.Embed(
                    name = "No permissions",
                    description = f"Cannot change {target}'s nickname."
                )
                forbidden_embed.set_footer(
                    text = "Insufficient permissions"
                )
                await ctx.send(embed = forbidden_embed)
        else:
            nickname_already_set_embed = discord.Embed(
                name = "Already have nickname",
                description = f"Your nickname is already {player_data['name']}."
            )
            nickname_already_set_embed.set_footer(
                text = core.static.wrist_spasm_disclaimer
            )
            await ctx.send(embed = nickname_already_set_embed)
        if prestige_role_object in ctx.author.roles:
            already_have_role_embed = discord.Embed(
                name = "Already have role",
                description = f"You already have the {prestige} Prestige role."
            )
            already_have_role_embed.set_footer(
                text = core.static.wrist_spasm_disclaimer
            )
            await ctx.send(embed = already_have_role_embed)
        else:
            await ctx.author.add_roles(prestige_role_object)
            added_role_embed = discord.Embed(
                name = "Added role",
                description = f"Gave you the {prestige} Prestige role."
            )
            added_role_embed.set_footer(
                text = core.static.wrist_spasm_disclaimer
            )
            await ctx.send(embed = added_role_embed)
        for role in self.roles:
            role_object = ctx.guild.get_role(self.roles[role])
            if (role_object in ctx.author.roles) and role_object is not prestige_role_object:
                await ctx.author.remove_roles(role_object)
                role_remove_embed = discord.Embed(
                    name = "Role removed",
                    description = f"Removed role <@{self.roles[role]}> from you."
                )
                role_remove_embed.set_footer(
                    text = f"{core.static.wrist_spasm_disclaimer}\n\
                    You are only supposed to have one Bedwars prestige role."
                )
                await ctx.send(embed = role_remove_embed)

    @wristspasm.command(name = "override")
    @commands.check(override_check)
    async def verify_override(self, ctx, target: discord.Member, ign):
        try:
            player_data = await core.minecraft.request.get_profile(ign)
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Verifying {target} as {player_data['name']}..."
            )
            loading_embed.set_footer(
                text = core.static.wrist_spasm_disclaimer
            )
            message = await ctx.send(embed = loading_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{ign}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            return
        try:
            player_stats = await self.player.get_player(player_data["uuid"])
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            return
        prestige = (await core.minecraft.hypixel.static.get_bedwars_prestige_data(player_stats["bedwars"]["star"]))["prestige"]
        prestige_role = self.roles[prestige]
        prestige_role_object = ctx.guild.get_role(prestige_role)
        if target.nick != player_data["name"]:
            try:
                await target.edit(nick = player_data["name"])
                nickname_changed_embed = discord.Embed(
                    name = "Nickname changed",
                    description = f"Changed {target}'s nickname to {player_data['name']}."
                    )
                nickname_changed_embed.set_footer(
                    text = core.static.wrist_spasm_disclaimer
                )
                await ctx.send(embed = nickname_changed_embed)
            except discord.errors.Forbidden:
                forbidden_embed = discord.Embed(
                    name = "No permissions",
                    description = f"Cannot change {target}'s nickname."
                )
                forbidden_embed.set_footer(
                    text = "Insufficient permissions"
                )
                await ctx.send(embed = forbidden_embed)
        else:
            nickname_already_set_embed = discord.Embed(
                name = "Already have nickname",
                description = f"{target}'s nickname is already {player_data['name']}."
            )
            nickname_already_set_embed.set_footer(
                text = core.static.wrist_spasm_disclaimer
            )
            await ctx.send(embed = nickname_already_set_embed)
        if prestige_role_object in target.roles:
            already_have_role_embed = discord.Embed(
                name = "Already have role",
                description = f"{target} already has the {prestige} Prestige role."
            )
            already_have_role_embed.set_footer(
                text = core.static.wrist_spasm_disclaimer
            )
            await ctx.send(embed = already_have_role_embed)
        else:
            await target.add_roles(prestige_role_object)
            added_role_embed = discord.Embed(
                name = "Added role",
                description = f"Gave {target} the {prestige} Prestige role."
            )
            added_role_embed.set_footer(
                text = core.static.wrist_spasm_disclaimer
            )
            await ctx.send(embed = added_role_embed)
        for role in self.roles:
            role_object = ctx.guild.get_role(self.roles[role])
            if (role_object in target.roles) and role_object is not prestige_role_object:
                await target.remove_roles(role_object)
                role_remove_embed = discord.Embed(
                    name = "Role removed",
                    description = f"Removed role <@{self.roles[role]}> from {target}."
                )
                role_remove_embed.set_footer(
                    text = f"{core.static.wrist_spasm_disclaimer}\n\
                    You are only supposed to have one Bedwars prestige role."
                )
                await ctx.send(embed = role_remove_embed)

def setup(bot):
    bot.add_cog(WristSpasm(bot))
    print("Reloaded cogs.wristspasm")

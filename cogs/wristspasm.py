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
from core.minecraft.request import MojangAPI

staff = [
    324025871255994368, # 10k
    324025871255994368, # CallLifeAlert
    436991256124588043, # _Disappointed
    259185628611215360, # FreakinDope
    328192039810236417, # x_10k (Sweet)
    465980302372634640, # freightcar
    368780147563823114 # MyerFire
]

async def staff_check(ctx):
    if ctx.author.id in staff:
        return True
    else:
        return False

class WristSpasm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bedwars = Bedwars()
        self.guild = 600311056627269642
        self.hypixel = core.minecraft.hypixel.request.HypixelAPI()
        self.mojang = MojangAPI()
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
            name = (await self.mojang.get_profile(player))['name']
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Verifying you as {name}..."
            )
            message = await ctx.send(embed = loading_embed)
            await self.hypixel.send_player_request(player)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            return
        prestige = (await self.bedwars.get_prestige_data())['prestige']
        prestige_role = self.roles[prestige]
        prestige_role_object = ctx.guild.get_role(prestige_role)
        if ctx.author.nick != name:
            await ctx.author.edit(nick = name)
            nickname_changed_embed = discord.Embed(
                name = "Nickname changed",
                description = f"Changed your nickname to {name}."
            )
            await ctx.send(embed = nickname_changed_embed)
        else:
            nickname_already_set_embed = discord.Embed(
                name = "Already have nickname",
                description = f"Your nickname is already {name}."
            )
            await ctx.send(embed = nickname_already_set_embed)
        if prestige_role_object in ctx.author.roles:
            already_have_role_embed = discord.Embed(
                name = "Already have role",
                description = f"You already have the {prestige} Prestige role."
            )
            await ctx.send(embed = already_have_role_embed)
            for role in self.roles:
                role_object = ctx.guild.get_role(self.roles[role])
                if (role_object in ctx.author.roles) and role_object != prestige_role_object:
                    role_remove_embed = discord.Embed(
                        name = "Role removed",
                        description = f"Removed role <@{self.roles[role]}> from you."
                    )
                    role_remove_embed.set_footer(
                        text = "You are only supposed to have one Bedwars prestige role."
                    )
                    await ctx.author.remove_roles(role_object)
                    await ctx.send(embed = role_remove_embed)
        else:
            for role in self.roles:
                role_object = ctx.guild.get_role(self.roles[role])
                if role_object in ctx.author.roles:
                    role_remove_embed = discord.Embed(
                        name = "Role removed",
                        description = f"Removed role <@{self.roles[role]}> from you."
                    )
                    role_remove_embed.set_footer(
                        text = "You are only supposed to have one Bedwars prestige role."
                    )
                    await ctx.author.remove_roles(role_object)
                    await ctx.send(embed = role_remove_embed)
            await ctx.author.add_roles(prestige_role_object)
            added_role_embed = discord.Embed(
                name = "Added role",
                description = f"Gave you the {prestige} Prestige role."
            )
            await ctx.send(embed = added_role_embed)

    @wristspasm.command(name = "override")
    @commands.check(staff_check)
    async def verify_override(self, ctx, target: discord.Member, ign):
        try:
            name = (await self.mojang.get_profile(ign))['name']
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Verifying {target} as {name}..."
            )
            message = await ctx.send(embed = loading_embed)
            await self.hypixel.send_player_request(ign)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{ign}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            return
        prestige = (await self.bedwars.get_prestige_data())['prestige']
        prestige_role = self.roles[prestige]
        prestige_role_object = ctx.guild.get_role(prestige_role)
        if target.nick != name:
            await target.edit(nick = name)
            nickname_changed_embed = discord.Embed(
                name = "Nickname changed",
                description = f"Changed {target}\'s nickname to {name}."
                )
            await ctx.send(embed = nickname_changed_embed)
        else:
            nickname_already_set_embed = discord.Embed(
                name = "Already have nickname",
                description = f"{target}\'s nickname is already {name}."
            )
            await ctx.send(embed = nickname_already_set_embed)
        if prestige_role_object in target.roles:
            already_have_role_embed = discord.Embed(
                name = "Already have role",
                description = f"{target} already has the {prestige} Prestige role."
            )
            await ctx.send(embed = already_have_role_embed)
            for role in self.roles:
                role_object = ctx.guild.get_role(self.roles[role])
                if (role_object in target.roles) and role_object != prestige_role_object:
                    role_remove_embed = discord.Embed(
                        name = "Role removed",
                        description = f"Removed role <@{self.roles[role]}> from {target}."
                    )
                    role_remove_embed.set_footer(
                        text = "You are only supposed to have one Bedwars prestige role."
                    )
                    await ctx.author.remove_roles(role_object)
                    await ctx.send(embed = role_remove_embed)
        else:
            for role in self.roles:
                role_object = ctx.guild.get_role(self.roles[role])
                if role_object in target.roles:
                    role_remove_embed = discord.Embed(
                        name = "Role removed",
                        description = f"Removed role <@{self.roles[role]}> from {target}."
                    )
                    role_remove_embed.set_footer(
                        text = "You are only supposed to have one Bedwars prestige role."
                    )
                    await ctx.author.remove_roles(role_object)
                    await ctx.send(embed = role_remove_embed)
            await ctx.author.add_roles(prestige_role_object)
            added_role_embed = discord.Embed(
                name = "Added role",
                description = f"Gave you the {prestige} Prestige role."
            )
            await ctx.send(embed = added_role_embed)

def setup(bot):
    bot.add_cog(WristSpasm(bot))
    print("Reloaded cogs.wristspasm")

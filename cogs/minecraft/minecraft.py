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
import datetime
import discord
from core.discord.markdown import Markdown
from core.minecraft.request import MojangAPI
from core.minecraft.verification.verification import Verification

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.markdown = Markdown()
        self.mojang = MojangAPI()
        self.verification = Verification()

    @commands.group(name = "minecraft", aliases = ["mc"], invoke_without_command = True)
    async def minecraft(self, ctx):
        return

    @minecraft.command(name = "name")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def name_history(self, ctx, player):
        index = 0
        try:
            player_data = await self.mojang.get_profile_name(player)
            name_history = await self.mojang.get_name_history_uuid(player_data['uuid'])
            name_history_embed = discord.Embed(
                name = "Name history"
            )
            for name in name_history:
                if index == 0: # First name does not have changedToAt attribute
                    name_history_embed.add_field(
                        name = f"Name #{index + 1}",
                        value = f"{name_history[index][0]} (Original)",
                        inline = False
                    )
                else:
                    name_history_embed.add_field(
                        name = f"Name #{index + 1}",
                        value = f"{name_history[index][0]} - {await self.markdown.italic(f'on {datetime.date.fromtimestamp((name_history[index][1]) / 1000)}')}",
                        inline = False
                    )
                index += 1
            await ctx.send(embed = name_history_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username."
            )
            await ctx.send(embed = nameerror_embed)

    @minecraft.command(name = "uuid")
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def uuid(self, ctx, *args):
        try:
            player = args[0]
            player_formatted_name = (await self.mojang.get_profile(player))['name']
            player_uuid = (await self.mojang.get_profile(player))['uuid']
        except IndexError: # If no arguments
            try:
                db_data = await self.verification.find_uuid(ctx.author.id)
                player_formatted_name = (await self.mojang.get_profile((db_data[0]['minecraft_uuid'])))['name']
                player_uuid = db_data[0]['minecraft_uuid']
            except IndexError:
                unverified_embed = discord.Embed(
                    name = "Not verified",
                    description = "You have to verify with `/mc verify <minecraft-ign>` first."
                )
                await ctx.send(embed = unverified_embed)
                return
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            return
        player_uuid_embed = discord.Embed(
            name = "Player UUID",
            description = f"{player_formatted_name}\'s UUID is {player_uuid}."
        )
        await ctx.send(embed = player_uuid_embed)

    @minecraft.command(name = "verify", aliases = ["link"])
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def verify(self, ctx, ign):
        try:
            player_data = await self.mojang.get_profile(ign)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{ign}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
        try:
            await self.verification.verify(ctx.author.id, f"{ctx.author.name}#{ctx.author.discriminator}", player_data['uuid'])
            verified_embed = discord.Embed(
                name = "Verified Minecraft IGN",
                description = f"Verified your Minecraft account as \"{player_data['name']}\""
            )
            verified_embed.set_footer(
                text = "... with Myaer."
            )
            await ctx.send(embed = verified_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['name']}\" does not seem to have Hypixel stats."
            )
            await ctx.send(embed = nameerror_embed)
            return
        except ValueError:
            already_has_discord_hypixel_embed = discord.Embed(
                name = "Already linked on Hypixel",
                description = f"{player_data['name']} has a linked Discord account on Hypixel that is not yours."
            )
            already_has_discord_hypixel_embed.set_footer(
                text = "If this is your Minecraft account, update your Discord name on Hypixel."
            )
            await ctx.send(embed = already_has_discord_hypixel_embed)
        except AttributeError:
            no_discord_hypixel_embed = discord.Embed(
                name = "No Discord linked on Hypixel",
                description = f"{player_data['name']} does not have a linked Discord name on Hypixel."
            )
            no_discord_hypixel_embed.set_footer(
                text = "Set your Discord name on Hypixel."
            )
            await ctx.send(embed = no_discord_hypixel_embed)

    @minecraft.command(name = "forceverify", aliases = ["forcelink"])
    @commands.is_owner()
    async def force_verify(self, ctx, target: discord.Member, ign):
        try:
            player_data = await self.mojang.get_profile(ign)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{ign}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            return
        await self.verification.force_verify(target.id, player_data['uuid'])
        verified_embed = discord.Embed(
            name = "Verified Minecraft IGN",
            description = f"Verified {target}\'s Minecraft account as \"{player_data['name']}\""
        )
        verified_embed.set_footer(
            text = "... with Myaer."
        )
        await ctx.send(embed = verified_embed)

    @minecraft.command(name = "unverify", aliases = ["unlink"])
    async def unverify(self, ctx):
        try:
            unverified_data = await self.verification.unverify(ctx.author.id)
            unverified_embed = discord.Embed(
                name = "Unverified",
                description = f"Unverified your Minecraft account \"{(await self.mojang.get_profile_uuid((unverified_data[0]['minecraft_uuid'])))['name']}\"."
            )
            unverified_embed.set_footer(
                text = f"UUID was {(await self.mojang.get_profile_uuid(unverified_data[0]['minecraft_uuid']))['uuid']}"
            )
            await ctx.send(embed = unverified_embed)
        except NameError:
            not_verified_embed = discord.Embed(
                name = "Not verified",
                description = "Your Minecraft account was not verified."
            )
            not_verified_embed.set_footer(
                text = "... with Myaer."
            )
            await ctx.send(embed = not_verified_embed)

    @minecraft.command(name = "forceunverify", aliases = ["forceunlink"])
    @commands.is_owner()
    async def force_unverify(self, ctx, target: discord.Member):
        try:
            unverified_data = await self.verification.unverify(target.id)
            unverified_embed = discord.Embed(
                name = "Unverified",
                description = f"Unverified {target}\'s Minecraft account \"{(await self.mojang.get_profile_uuid((unverified_data[0]['minecraft_uuid'])))['name']}\"."
            )
            unverified_embed.set_footer(
                text = f"UUID was {(await self.mojang.get_profile_uuid(unverified_data[0]['minecraft_uuid']))['uuid']}"
            )
            await ctx.send(embed = unverified_embed)
        except NameError:
            not_verified_embed = discord.Embed(
                name = "Not verified",
                description = f"{target}\'s Minecraft account was not verified."
            )
            not_verified_embed.set_footer(
                text = "... with Myaer."
            )
            await ctx.send(embed = not_verified_embed)

def setup(bot):
    bot.add_cog(Minecraft(bot))
    print("Reloaded cogs.minecraft")

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
import humanfriendly
from core.discord.markdown import Markdown
from core.minecraft.request import MojangAPI
import sys
import traceback
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
    async def name_history(self, ctx, *args):
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
        loading_embed = discord.Embed(
            name = "Loading",
            description = f"Loading {player_formatted_name}\'s name history..."
        )
        message = await ctx.send(embed = loading_embed)
        index = 0
        name_history = await self.mojang.get_name_history_uuid(player_uuid)
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
        await message.edit(embed = name_history_embed)

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
        loading_embed = discord.Embed(
            name = "Loading",
            description = f"Loading {player_formatted_name}\'s WLR data..."
        )
        message = await ctx.send(embed = loading_embed)
        player_uuid_embed = discord.Embed(
            name = "Player UUID",
            description = f"{player_formatted_name}\'s UUID is {player_uuid}."
        )
        await message.edit(embed = player_uuid_embed)

    @minecraft.command(name = "verify", aliases = ["link"])
    @commands.cooldown(1, 60, commands.BucketType.guild)
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
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Verifying you as {player_data['name']}..."
            )
            message = await ctx.send(embed = loading_embed)
            await self.verification.verify(ctx.author.id, f"{ctx.author.name}#{ctx.author.discriminator}", player_data['uuid'])
            verified_embed = discord.Embed(
                name = "Verified Minecraft IGN",
                description = f"Verified your Minecraft account as \"{player_data['name']}\""
            )
            verified_embed.set_footer(
                text = "... with Myaer."
            )
            await message.edit(embed = verified_embed)
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_data['name']}\" does not seem to have Hypixel stats."
            )
            await message.edit(embed = nameerror_embed)
            raise NameError("Invalid input")
            return
        except ValueError:
            already_has_discord_hypixel_embed = discord.Embed(
                name = "Already linked on Hypixel",
                description = f"{player_data['name']} has a linked Discord account on Hypixel that is not yours."
            )
            already_has_discord_hypixel_embed.set_footer(
                text = "If this is your Minecraft account, update your Discord name on Hypixel."
            )
            await message.edit(embed = already_has_discord_hypixel_embed)
            raise ValueError("Already linked on Hypixel")
            return
        except AttributeError:
            no_discord_hypixel_embed = discord.Embed(
                name = "No Discord linked on Hypixel",
                description = f"{player_data['name']} does not have a linked Discord name on Hypixel."
            )
            no_discord_hypixel_embed.set_footer(
                text = "Set your Discord name on Hypixel."
            )
            await message.edit(embed = no_discord_hypixel_embed)
            raise AttributeError("No Discord linked on Hypixel")
            return

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
        loading_embed = discord.Embed(
            name = "Loading",
            description = f"Verifying {target} as {player_data['name']}..."
        )
        message = await ctx.send(embed = loading_embed)
        await self.verification.force_verify(target.id, player_data['uuid'])
        verified_embed = discord.Embed(
            name = "Verified Minecraft IGN",
            description = f"Verified {target}\'s Minecraft account as \"{player_data['name']}\""
        )
        verified_embed.set_footer(
            text = "... with Myaer."
        )
        await message.edit(embed = verified_embed)

    @minecraft.command(name = "unverify", aliases = ["unlink"])
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def unverify(self, ctx):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Unverifying you..."
            )
            message = await ctx.send(embed = loading_embed)
            unverified_data = await self.verification.unverify(ctx.author.id)
            unverified_embed = discord.Embed(
                name = "Unverified",
                description = f"Unverified your Minecraft account \"{(await self.mojang.get_profile_uuid((unverified_data[0]['minecraft_uuid'])))['name']}\"."
            )
            unverified_embed.set_footer(
                text = f"UUID was {(await self.mojang.get_profile_uuid(unverified_data[0]['minecraft_uuid']))['uuid']}"
            )
            await message.edit(embed = unverified_embed)
        except NameError:
            not_verified_embed = discord.Embed(
                name = "Not verified",
                description = "Your Minecraft account was not verified."
            )
            not_verified_embed.set_footer(
                text = "... with Myaer."
            )
            await message.edit(embed = not_verified_embed)

    @minecraft.command(name = "forceunverify", aliases = ["forceunlink"])
    @commands.is_owner()
    async def force_unverify(self, ctx, target: discord.Member):
        try:
            loading_embed = discord.Embed(
                name = "Loading",
                description = f"Unverifying {target}\'s Minecraft account..."
            )
            message = await ctx.send(embed = loading_embed)
            unverified_data = await self.verification.unverify(target.id)
            unverified_embed = discord.Embed(
                name = "Unverified",
                description = f"Unverified {target}\'s Minecraft account \"{(await self.mojang.get_profile_uuid((unverified_data[0]['minecraft_uuid'])))['name']}\"."
            )
            unverified_embed.set_footer(
                text = f"UUID was {(await self.mojang.get_profile_uuid(unverified_data[0]['minecraft_uuid']))['uuid']}"
            )
            await message.edit(embed = unverified_embed)
        except NameError:
            not_verified_embed = discord.Embed(
                name = "Not verified",
                description = f"{target}\'s Minecraft account was not verified."
            )
            not_verified_embed.set_footer(
                text = "... with Myaer."
            )
            await message.edit(embed = not_verified_embed)

    async def cog_command_error(self, ctx, error):

        error = getattr(error, "original", error)

        if (isinstance(error, NameError)) or (isinstance(error, ValueError)) or (isinstance(error, AttributeError)):
            await ctx.command.reset_cooldown(ctx)
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = datetime.timedelta(seconds = error.retry_after)
            cooldown_embed = discord.Embed(
                name = "Cooldown",
                color = ctx.author.color,
                description = f"Verification commands should not need to be used this often. Try again in {humanfriendly.format_timespan(cooldown)}"
            )
            await ctx.send(embed = cooldown_embed)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(Minecraft(bot))
    print("Reloaded cogs.minecraft")

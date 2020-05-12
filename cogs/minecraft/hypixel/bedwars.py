from core.minecraft.hypixel.bedwars import Bedwars
from core.config import Config
from discord.ext import commands
import discord
from core.minecraft.hypixel.hypixel import Hypixel
from core.minecraft.minecraft import Minecraft

class BedwarsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()
        self.bedwars = Bedwars()
        self.hypixel = Hypixel()
        self.minecraft = Minecraft()

    @commands.command(name="bw", aliases=["bwstats"])
    async def get_stats(self, ctx, player):
        try:
            await self.hypixel.send_request(player) # Sets global variable player_json in core.minecraft.hypixel
            player_stats_embed = discord.Embed(
                title = f"{(await self.minecraft.get_profile(player))['name']}\'s Bedwars Stats",
                color = int((await self.bedwars.get_prestige_data(player))['prestige_color'], 16) # 16 - Hex value.
            )
            player_stats_embed.add_field(
                name = "Level",
                value = f"{await self.bedwars.get_star(player)} ({(await self.bedwars.get_prestige_data(player))['prestige']} Prestige)",
                inline = False
            )
            player_stats_embed.add_field(
                name = "Final Kills",
                value = f"{await self.bedwars.get_final_kills(player)}"
            )
            player_stats_embed.add_field(
                name = "Final Deaths",
                value = f"{await self.bedwars.get_final_deaths(player)}"
            )
            player_stats_embed.add_field(
                name = "FKDR",
                value = f"{await self.bedwars.get_fkdr(player)}"
            )
            player_stats_embed.add_field(
                name = "Beds Broken",
                value = f"{await self.bedwars.get_beds_broken(player)}"
            )
            player_stats_embed.add_field(
                name = "Beds Lost",
                value = f"{await self.bedwars.get_beds_lost(player)}"
            )
            player_stats_embed.add_field(
                name = "BBLR",
                value = f"{await self.bedwars.get_bblr(player)}"
            )
            player_stats_embed.add_field(
                name = "Wins",
                value = f"{await self.bedwars.get_wins(player)}"
            )
            player_stats_embed.add_field(
                name = "Losses",
                value = f"{await self.bedwars.get_losses(player)}"
            )
            player_stats_embed.add_field(
                name = "WLR",
                value = f"{await self.bedwars.get_wlr(player)}"
            )
            await ctx.send(embed=player_stats_embed)
        except NameError:
            await ctx.send(f"Player \"{player}\" does not exist!")

def setup(bot):
    bot.add_cog(BedwarsCommands(bot))
    print("Reloaded cogs.minecraft.hypixel.bedwars")

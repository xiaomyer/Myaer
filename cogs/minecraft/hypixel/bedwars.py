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
    async def get_bedwars_stats(self, ctx, player):
#        try:
        await self.hypixel.send_request(player)
        player_display_name = (await self.minecraft.get_profile(player))["name"]
        player_bedwars_star = await self.bedwars.get_bedwars_star(player)
        player_bedwars_prestige = (await self.bedwars.get_bedwars_prestige_data(player))["bedwars_prestige"]
        player_bedwars_prestige_color = (await self.bedwars.get_bedwars_prestige_data(player))["bedwars_prestige_color"]
        player_bedwars_final_kills = await self.bedwars.get_bedwars_final_kills(player)
        player_bedwars_final_deaths = await self.bedwars.get_bedwars_final_deaths(player)
        player_bedwars_fkdr = await self.bedwars.get_bedwars_fkdr(player)

        player_bedwars_stats = discord.Embed(
            title = f"{player_display_name}'s Bedwars Stats",
            color = int(player_bedwars_prestige_color, 16) # 16 - Hex value.
        )
        player_bedwars_stats.add_field(
            name = "Level",
            value = f"{player_bedwars_star} ({player_bedwars_prestige} Prestige)",
            inline = False
        )
        player_bedwars_stats.add_field(
            name = "Final Kills",
            value = f"{player_bedwars_final_kills}"
        )
        player_bedwars_stats.add_field(
            name = "Final Deaths",
            value = f"{player_bedwars_final_deaths}"
        )
        player_bedwars_stats.add_field(
            name = "FKDR",
            value = f"{player_bedwars_fkdr}"
        )
        await ctx.send(embed=player_bedwars_stats)
#        except NameError:
#            await ctx.send("Unknown player!")

def setup(bot):
    bot.add_cog(BedwarsCommands(bot))
    print("Reloaded cogs.minecraft.hypixel.bedwars")

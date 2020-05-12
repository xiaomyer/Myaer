import json
import core.minecraft.hypixel.hypixel

bedwars_prestige_colors = {
    "Stone" : "607D8B",
    "Iron" : "95A5A6",
    "Gold" : "FFAC0F",
    "Diamond" : "55FFFF",
    "Emerald" : "00AA00",
    "Sapphire" : "00AAAA",
    "Ruby" : "AA0000",
    "Crystal" : "FF69DC",
    "Opal" : "2562E9",
    "Amethyst" : "AA00AA",
    "Rainbow" : "FF69DC"
}

class Bedwars():
    async def get_bedwars_star(self, player):
        bedwars_star = core.minecraft.hypixel.hypixel.player_json["player"]["achievements"]["bedwars_level"]
        return bedwars_star

    async def get_bedwars_prestige_data(self, player):
        bedwars_star = await self.get_bedwars_star(player)
        if bedwars_star in range(0, 99):
            bedwars_prestige = "Stone"
            bedwars_prestige_color = bedwars_prestige_colors["Stone"]
        elif bedwars_star in range(100, 199):
            bedwars_prestige = "Iron"
            bedwars_prestige_color = bedwars_prestige_colors["Iron"]
        elif bedwars_star in range(200, 299):
            bedwars_prestige = "Gold"
            bedwars_prestige_color = bedwars_prestige_colors["Gold"]
        elif bedwars_star in range(300, 399):
            bedwars_prestige = "Diamond"
            bedwars_prestige_color = bedwars_prestige_colors["Diamond"]
        elif bedwars_star in range(400, 499):
            bedwars_prestige = "Emerald"
            bedwars_prestige_color = bedwars_prestige_colors["Emerald"]
        elif bedwars_star in range(500, 599):
            bedwars_prestige = "Sapphire"
            bedwars_prestige_color = bedwars_prestige_colors["Sapphire"]
        elif bedwars_star in range(600, 699):
            bedwars_prestige = "Ruby"
            bedwars_prestige_color = bedwars_prestige_colors["Ruby"]
        elif bedwars_star in range(700, 799):
            bedwars_prestige = "Crystal"
            bedwars_prestige_color = bedwars_prestige_colors["Crystal"]
        elif bedwars_star in range(800, 899):
            bedwars_prestige = "Opal"
            bedwars_prestige_color = bedwars_prestige_colors["Opal"]
        elif bedwars_star in range(900, 999):
            bedwars_prestige = "Amethyst"
            bedwars_prestige_color = bedwars_prestige_colors["Amethyst"]
        else:
            bedwars_prestige = "Rainbow"
            bedwars_prestige_color = bedwars_prestige_colors["Rainbow"]

        bedwars_prestige_data = {
            "bedwars_prestige" : f"{bedwars_prestige}",
            "bedwars_prestige_color" : f"{bedwars_prestige_color}"
        }
        return bedwars_prestige_data

    async def get_bedwars_final_kills(self, player):
        try:
            final_kills = core.minecraft.hypixel.hypixel.player_json["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
            return final_kills
        except KeyError:
            return 0

    async def get_bedwars_final_deaths(self, player):
        try:
            final_deaths = core.minecraft.hypixel.hypixel.player_json["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
            return final_deaths
        except KeyError:
            return 0

    async def get_bedwars_fkdr(self, player):
        final_kills = await self.get_bedwars_final_kills(player)
        final_deaths = await self.get_bedwars_final_deaths(player)

        fkdr = final_kills / final_deaths
        return round(fkdr, 2)

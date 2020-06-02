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

import math

prestige_colors = {
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
    "Rainbow" : "1ABC9C"
}

prestiges = [
    "Stone",
    "Iron",
    "Gold",
    "Diamond",
    "Emerald",
    "Sapphire",
    "Ruby",
    "Crystal",
    "Opal",
    "Amethyst",
    "Rainbow"
]

rank_colors = {
    "VIP" : "55FF55",
    "VIP+" : "55FF55",
    "MVP" : "55FFFF",
    "MVP+" : "55FFFF",
    "MVP++" : "FFAA00",
    "YOUTUBE" : "FF5555",
    "HELPER" : "5555FF",
    "MOD" : "00AA00",
    "ADMIN" : "AA0000",
    None : "607D8B"
}

class HypixelStatic():
    async def get_network_level_data(self, experience):
        level = (math.sqrt(experience + 15312.5) - 88.38834764831843) / 35.35533905932738 # formula that i don't understand, something to do with square roots - thank you @littlemissantivirus
        level_data = {
            "level" : math.trunc(level),
            "percentage" : round((level - math.trunc(level)) * 100, 2)
        }
        return level_data

    async def get_rank_data(self, rank, monthly_package_rank, new_package_rank, package_rank): # complicated because returning the formatted rank name
        formatted_rank = None
        if rank:
            if rank == "YOUTUBER":
                formatted_rank = "YOUTUBE"
            elif rank == "HELPER":
                formatted_rank = "HELPER"
            elif rank == "MODERATOR":
                formatted_rank = "MOD"
            elif rank == "ADMIN":
                formatted_rank = "ADMIN"

        elif monthly_package_rank and not formatted_rank:
            if monthly_package_rank == "SUPERSTAR": # hypixel i am questioning you greatly
                formatted_rank = "MVP++"

        if new_package_rank and not formatted_rank:
            if new_package_rank == "NONE":
                formatted_rank = None
            elif new_package_rank == "VIP":
                formatted_rank = "VIP"
            elif new_package_rank == "VIP_PLUS":
                formatted_rank = "VIP+"
            elif new_package_rank == "MVP":
                formatted_rank = "MVP"
            elif new_package_rank == "MVP_PLUS":
                formatted_rank = "MVP+"

        elif package_rank and not formatted_rank:
            if package_rank == "NONE":
                formatted_rank = None
            elif package_rank == "VIP":
                formatted_rank = "VIP"
            elif package_rank == "VIP_PLUS":
                formatted_rank = "VIP+"
            elif package_rank == "MVP":
                formatted_rank = "MVP"
            elif package_rank == "MVP_PLUS":
                formatted_rank = "MVP+"

        rank_data = {
            "rank" : formatted_rank,
            "color" : rank_colors[formatted_rank]
        }
        return rank_data

    async def get_ratio(self, positive_stat, negative_stat):
        try:
            ratio = positive_stat / negative_stat
            return round(ratio, 2)
        except ZeroDivisionError:
            if positive_stat > 0:
                return float("inf")
            else:
                return 0

    async def get_increase_stat(self, positive_stat, negative_stat, increase):
        # positive_stat is a "good" stat like final_kills
        # negative_stat is a "bad" stat like final_deaths
        # increase is the amount the positive_stat to negative_stat ratio needs to increase
        try:
            stat = positive_stat / negative_stat
            needed = (stat + increase) * negative_stat - positive_stat
            return round(needed)
        except ZeroDivisionError:
            if positive_stat > 0:
                return float("inf")
            else:
                return 0

    async def get_bedwars_prestige_data(self, star):
        star_rounded = star // 100 # // is floor division, basically math.floor(await self.get_star() / 100)
        star_rounded = star_rounded if star_rounded < 10 else 10 # if greater than 10, set to ten
        return {"prestige": prestiges[star_rounded], "prestige_color": prestige_colors[prestiges[star_rounded]]} # based on order of prestiges and prestige colors

    async def get_skywars_prestige_data(self, star):
        if star in range(0, 5):
            prestige = "Stone"
            prestige_color = prestige_colors["Stone"]
        elif star in range(5, 10):
            prestige = "Iron"
            prestige_color = prestige_colors["Iron"]
        elif star in range(10, 15):
            prestige = "Gold"
            prestige_color = prestige_colors["Gold"]
        elif star in range(15, 20):
            prestige = "Diamond"
            prestige_color = prestige_colors["Diamond"]
        elif star in range(20, 25):
            prestige = "Emerald"
            prestige_color = prestige_colors["Emerald"]
        elif star in range(25, 30):
            prestige = "Sapphire"
            prestige_color = prestige_colors["Sapphire"]
        elif star in range(30, 35):
            prestige = "Ruby"
            prestige_color = prestige_colors["Ruby"]
        elif star in range(35, 40):
            prestige = "Crystal"
            prestige_color = prestige_colors["Crystal"]
        elif star in range(40, 45):
            prestige = "Opal"
            prestige_color = prestige_colors["Opal"]
        elif star in range(45, 50):
            prestige = "Amethyst"
            prestige_color = prestige_colors["Amethyst"]
        elif star in range(50, 60):
            prestige = "Rainbow"
            prestige_color = prestige_colors["Rainbow"]
        else:
            prestige = "Mystic"
            prestige_color = prestige_colors["Rainbow"]

        prestige_data = {
            "prestige" : prestige,
            "prestige_color" : prestige_color
        }
        return prestige_data

    async def get_skywars_star_from_experience(self, experience): # another formula that I don't understand, thanks to @GamingGeeek and @littlemissantivirus
        total_xp = [20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
        star = 0
        if experience >= 15000:
            return (experience - 15000) / 10000 + 12
        else:
            c = 0
            while experience >= 0 and c < len(total_xp):
                if experience - total_xp[c] >= 0:
                    c += 1
                else:
                    star = c + 1 + (experience - total_xp[c - 1]) / (total_xp[c] - total_xp[c - 1])
                    break
        return star

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

import json
import math
import core.minecraft.hypixel.request

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
    "Rainbow" : "FF69DC"
}

class Skywars():
    async def get_star_experience(self, experience): # Formula that I don't understand, thanks to @GamingGeeek and littlemissantivirus
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

    async def get_star(self):
        skywars_experience = core.minecraft.hypixel.request.player_json['player']['stats']['SkyWars']['skywars_experience']
        star = await self.get_star_experience(skywars_experience)
        return math.trunc(star)

    async def get_prestige_data(self):
        star = await self.get_star()
        if star in range(0, 5):
            prestige = "Stone"
            prestige_color = prestige_colors['Stone']
        elif star in range(5, 10):
            prestige = "Iron"
            prestige_color = prestige_colors['Iron']
        elif star in range(10, 15):
            prestige = "Gold"
            prestige_color = prestige_colors['Gold']
        elif star in range(15, 20):
            prestige = "Diamond"
            prestige_color = prestige_colors['Diamond']
        elif star in range(20, 25):
            prestige = "Emerald"
            prestige_color = prestige_colors['Emerald']
        elif star in range(25, 30):
            prestige = "Sapphire"
            prestige_color = prestige_colors['Sapphire']
        elif star in range(30, 35):
            prestige = "Ruby"
            prestige_color = prestige_colors['Ruby']
        elif star in range(35, 40):
            prestige = "Crystal"
            prestige_color = prestige_colors['Crystal']
        elif star in range(40, 45):
            prestige = "Opal"
            prestige_color = prestige_colors['Opal']
        elif star in range(45, 50):
            prestige = "Amethyst"
            prestige_color = prestige_colors['Amethyst']
        elif star in range(50, 60):
            prestige = "Rainbow"
            prestige_color = prestige_colors['Rainbow']
        else:
            prestige = "Mystic"
            prestige_color = prestige_colors['Rainbow']

        prestige_data = {
            "prestige" : prestige,
            "prestige_color" : prestige_color
        }
        return prestige_data

    async def get_games_played(self):
        games_played = core.minecraft.hypixel.request.player_json['player']['stats']['SkyWars']['games_played_skywars']
        return games_played

    async def get_coins(self):
        coins = core.minecraft.hypixel.request.player_json['player']['stats']['SkyWars']['coins']
        return coins

    async def get_tokens(self):
        tokens = core.minecraft.hypixel.request.player_json['player']['stats']['SkyWars']['cosmetic_tokens']
        return tokens

    async def get_souls(self):
        souls = core.minecraft.hypixel.request.player_json['player']['stats']['SkyWars']['souls']
        return souls

    async def get_ratio(self, positive_stat, negative_stat):
        ratio = positive_stat / negative_stat
        return round(ratio, 2)

    async def get_kills(self):
        kills = core.minecraft.hypixel.request.player_json['player']['stats']['SkyWars']['kills']
        return kills

    async def get_deaths(self):
        deaths = core.minecraft.hypixel.request.player_json['player']['stats']['SkyWars']['deaths']
        return deaths

    async def get_wins(self):
        wins = core.minecraft.hypixel.request.player_json['player']['stats']['SkyWars']['wins']
        return wins

    async def get_losses(self):
        losses = core.minecraft.hypixel.request.player_json['player']['stats']['SkyWars']['losses']
        return losses

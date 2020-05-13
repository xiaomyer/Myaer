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
import core.minecraft.hypixel.hypixel

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

class Bedwars():
    async def get_star(self, player):
        star = core.minecraft.hypixel.hypixel.player_json['player']['achievements']['bedwars_level'] # what the fuck why is bedwars_level in achievements bruh
        return star

    async def get_prestige_data(self, player):
        star = await self.get_star(player)
        if star in range(0, 99):
            prestige = 'Stone'
            prestige_color = prestige_colors['Stone']
        elif star in range(100, 199):
            prestige = 'Iron'
            prestige_color = prestige_colors['Iron']
        elif star in range(200, 299):
            prestige = 'Gold'
            prestige_color = prestige_colors['Gold']
        elif star in range(300, 399):
            prestige = 'Diamond'
            prestige_color = prestige_colors['Diamond']
        elif star in range(400, 499):
            prestige = 'Emerald'
            prestige_color = prestige_colors['Emerald']
        elif star in range(500, 599):
            prestige = 'Sapphire'
            prestige_color = prestige_colors['Sapphire']
        elif star in range(600, 699):
            prestige = 'Ruby'
            prestige_color = prestige_colors['Ruby']
        elif star in range(700, 799):
            prestige = 'Crystal'
            prestige_color = prestige_colors['Crystal']
        elif star in range(800, 899):
            prestige = 'Opal'
            prestige_color = prestige_colors['Opal']
        elif star in range(900, 999):
            prestige = 'Amethyst'
            prestige_color = prestige_colors['Amethyst']
        else:
            prestige = 'Rainbow'
            prestige_color = prestige_colors['Rainbow']

        prestige_data = {
            "prestige" : f"{prestige}",
            "prestige_color" : f"{prestige_color}"
        }
        return prestige_data

    async def get_games_played(self, player):
        try:
            games_played = core.minecraft.hypixel.hypixel.player_json['player']['stats']['Bedwars']['games_played_bedwars']
            return games_played
        except KeyError:
            return 0

    async def get_coins(self, player):
        try:
            coins = core.minecraft.hypixel.hypixel.player_json['player']['stats']['Bedwars']['coins_bedwars']
            return coins
        except KeyError:
            return 0

    async def get_final_kills(self, player):
        try:
            final_kills = core.minecraft.hypixel.hypixel.player_json['player']['stats']['Bedwars']['final_kills_bedwars']
            return final_kills
        except KeyError:
            return 0

    async def get_final_deaths(self, player):
        try:
            final_deaths = core.minecraft.hypixel.hypixel.player_json['player']['stats']['Bedwars']['final_deaths_bedwars']
            return final_deaths
        except KeyError:
            return 0

    async def get_fkdr(self, player):
        final_kills = await self.get_final_kills(player)
        final_deaths = await self.get_final_deaths(player)

        fkdr = final_kills / final_deaths
        return round(fkdr, 2)

    async def get_increase_fkdr(self, player, increase): # Calculates how many finals it would take to increase player's FKDR by one
        final_kills = await self.get_final_kills(player)
        final_deaths = await self.get_final_deaths(player)
        fkdr = await self.get_fkdr(player)

        needed = (fkdr + increase) * final_deaths - final_kills
        return round(needed)

    async def get_increase_stat(self, player, positive_stat, negative_stat, increase):
        # positive_stat is a "good" stat like final_kills
        # negative_stat is a "bad" stat like final_deaths
        # increase is the amount the positive_stat to negative_stat ratio needs to increase
        stat = positive_stat / negative_stat
        needed = (stat + increase) * negative_stat - positive_stat
        return round(needed)

    async def get_beds_broken(self, player):
        try:
            beds_broken = core.minecraft.hypixel.hypixel.player_json['player']['stats']['Bedwars']['beds_broken_bedwars']
            return beds_broken
        except KeyError:
            return 0

    async def get_beds_lost(self, player):
        try:
            beds_lost = core.minecraft.hypixel.hypixel.player_json['player']['stats']['Bedwars']['beds_lost_bedwars']
            return beds_lost
        except KeyError:
            return 0

    async def get_bblr(self, player):
        beds_broken = await self.get_beds_broken(player)
        beds_lost = await self.get_beds_lost(player)

        bblr = beds_broken / beds_lost
        return round(bblr, 2)

    async def get_increase_bblr(self, player, increase): # Calculates how many finals it would take to increase player's FKDR by one
        beds_broken = await self.get_beds_broken(player)
        beds_lost = await self.get_beds_lost(player)
        bblr = await self.get_bblr(player)

        needed = (bblr + increase) * beds_lost - beds_broken
        return round(needed)

    async def get_wins(self, player):
        try:
            wins = core.minecraft.hypixel.hypixel.player_json['player']['stats']['Bedwars']['wins_bedwars']
            return wins
        except KeyError:
            return 0

    async def get_losses(self, player):
        try:
            losses = core.minecraft.hypixel.hypixel.player_json['player']['stats']['Bedwars']['losses_bedwars']
            return losses
        except KeyError:
            return 0

    async def get_wlr(self, player):
        wins = await self.get_wins(player)
        losses = await self.get_losses(player)

        wlr = wins / losses
        return round(wlr, 2)

    async def get_increase_wlr(self, player, increase):
        wins = await self.get_wins(player)
        losses = await self.get_losses(player)
        wlr = await self.get_wlr(player)

        needed = (wlr + increase) * wins - losses
        return round(needed)

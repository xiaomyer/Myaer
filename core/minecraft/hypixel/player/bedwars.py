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

class Bedwars():
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

    async def get_star(self):
        try:
            star = core.minecraft.hypixel.request.player_json['player']['achievements']['bedwars_level'] # what the fuck why is bedwars_level in achievements bruh
            return star
        except KeyError:
            return 0

    async def get_prestige_data(self):
        star_rounded = await self.get_star() // 100 # // = floor division, basically math.floor(await self.get_star() / 100)
        star_rounded = star_rounded if star_rounded < 10 else 10 # if greater than 10, set to ten
        prestiges = ['Stone', 'Iron', 'Gold', 'Diamond', 'Emerald', 'Sapphire', 'Ruby', 'Opal', 'Amethyst', 'Rainbow']
        return {"prestige": prestiges[star_rounded], "prestige_color": prestige_colors[prestiges[star_rounded]]} # sometimes my genius, it's...it's almost frightnening

    async def get_coins(self):
        try:
            coins = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['coins_bedwars']
            return coins
        except KeyError:
            return 0

    async def get_games_played(self):
        try:
            games_played = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['games_played_bedwars']
            return games_played
        except KeyError:
            return 0

    async def get_solo_games_played(self):
        try:
            solo_games_played = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_one_games_played_bedwars']
            return solo_games_played
        except KeyError:
            return 0

    async def get_doubles_games_played(self):
        try:
            doubles_games_played = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_two_games_played_bedwars']
            return doubles_games_played
        except KeyError:
            return 0

    async def get_threes_games_played(self):
        try:
            threes_games_played = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_three_games_played_bedwars']
            return solo_games_played
        except KeyError:
            return 0

    async def get_fours_games_played(self):
        try:
            fours_games_played = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_four_games_played_bedwars']
            return fours_games_played
        except KeyError:
            return 0

    async def get_four_v_four_games_played(self):
        try:
            four_v_four_games_played = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['two_four_games_played_bedwars']
            return four_v_four_games_played
        except KeyError:
            return 0

    async def get_final_kills(self):
        try:
            final_kills = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['final_kills_bedwars']
            return final_kills
        except KeyError:
            return 0

    async def get_solo_final_kills(self):
        try:
            solo_final_kills = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_one_final_kills_bedwars']
            return solo_final_kills
        except KeyError:
            return 0

    async def get_doubles_final_kills(self):
        try:
            doubles_final_kills = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_two_final_kills_bedwars']
            return doubles_final_kills
        except KeyError:
            return 0

    async def get_threes_final_kills(self):
        try:
            threes_final_kills = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_three_final_kills_bedwars']
            return threes_final_kills
        except KeyError:
            return 0

    async def get_fours_final_kills(self):
        try:
            fours_final_kills = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_four_final_kills_bedwars']
            return fours_final_kills
        except KeyError:
            return 0

    async def get_four_v_four_final_kills(self):
        try:
            four_v_four_final_kills = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['two_four_final_kills_bedwars']
            return four_v_four_final_kills
        except KeyError:
            return 0

    async def get_final_deaths(self):
        try:
            final_deaths = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['final_deaths_bedwars']
            return final_deaths
        except KeyError:
            return 0

    async def get_solo_final_deaths(self):
        try:
            solo_final_deaths = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_one_final_deaths_bedwars']
            return solo_final_deaths
        except KeyError:
            return 0

    async def get_doubles_final_deaths(self):
        try:
            doubles_final_deaths = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_two_final_deaths_bedwars']
            return doubles_final_deaths
        except KeyError:
            return 0

    async def get_threes_final_deaths(self):
        try:
            threes_final_deaths = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_three_final_deaths_bedwars']
            return threes_final_deaths
        except KeyError:
            return 0

    async def get_fours_final_deaths(self):
        try:
            fours_final_deaths = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_four_final_deaths_bedwars']
            return fours_final_deaths
        except KeyError:
            return 0

    async def get_four_v_four_final_deaths(self):
        try:
            four_v_four_final_deaths = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['two_four_final_deaths_bedwars']
            return four_v_four_final_deaths
        except KeyError:
            return 0

    async def get_beds_broken(self):
        try:
            beds_broken = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['beds_broken_bedwars']
            return beds_broken
        except KeyError:
            return 0

    async def get_solo_beds_broken(self):
        try:
            solo_beds_broken = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_one_beds_broken_bedwars']
            return solo_beds_broken
        except KeyError:
            return 0

    async def get_doubles_beds_broken(self):
        try:
            doubles_beds_broken = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_two_beds_broken_bedwars']
            return doubles_beds_broken
        except KeyError:
            return 0

    async def get_threes_beds_broken(self):
        try:
            threes_beds_broken = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_three_beds_broken_bedwars']
            return threes_beds_broken
        except KeyError:
            return 0

    async def get_fours_beds_broken(self):
        try:
            fours_beds_broken = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_four_beds_broken_bedwars']
            return fours_beds_broken
        except KeyError:
            return 0

    async def get_four_v_four_beds_broken(self):
        try:
            four_v_four_beds_broken = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['two_four_beds_broken_bedwars']
            return four_v_four_beds_broken
        except KeyError:
            return 0

    async def get_beds_lost(self):
        try:
            beds_lost = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['beds_lost_bedwars']
            return beds_lost
        except KeyError:
            return 0

    async def get_solo_beds_lost(self):
        try:
            solo_beds_lost = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_one_beds_lost_bedwars']
            return solo_beds_lost
        except KeyError:
            return 0

    async def get_doubles_beds_lost(self):
        try:
            doubles_beds_lost = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_two_beds_lost_bedwars']
            return doubles_beds_lost
        except KeyError:
            return 0

    async def get_threes_beds_lost(self):
        try:
            threes_beds_lost = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_three_beds_lost_bedwars']
            return threes_beds_lost
        except KeyError:
            return 0

    async def get_fours_beds_lost(self):
        try:
            fours_beds_lost = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_four_beds_lost_bedwars']
            return fours_beds_lost
        except KeyError:
            return 0

    async def get_four_v_four_beds_lost(self):
        try:
            four_v_four_beds_lost = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['two_four_beds_lost_bedwars']
            return four_v_four_beds_lost
        except KeyError:
            return 0

    async def get_wins(self):
        try:
            wins = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['wins_bedwars']
            return wins
        except KeyError:
            return 0

    async def get_solo_wins(self):
        try:
            solo_wins = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_one_wins_bedwars']
            return solo_wins
        except KeyError:
            return 0

    async def get_doubles_wins(self):
        try:
            doubles_wins = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_two_wins_bedwars']
            return doubles_wins
        except KeyError:
            return 0

    async def get_threes_wins(self):
        try:
            threes_wins = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_three_wins_bedwars']
            return threes_wins
        except KeyError:
            return 0

    async def get_fours_wins(self):
        try:
            fours_wins = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_four_wins_bedwars']
            return fours_wins
        except KeyError:
            return 0

    async def get_four_v_four_wins(self):
        try:
            four_v_four_wins = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['two_four_wins_bedwars']
            return four_v_four_wins
        except KeyError:
            return 0

    async def get_losses(self):
        try:
            losses = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['losses_bedwars']
            return losses
        except KeyError:
            return 0

    async def get_solo_losses(self):
        try:
            solo_losses = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_one_losses_bedwars']
            return solo_losses
        except KeyError:
            return 0

    async def get_doubles_losses(self):
        try:
            doubles_losses = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['eight_two_losses_bedwars']
            return doubles_losses
        except KeyError:
            return 0

    async def get_threes_losses(self):
        try:
            threes_losses = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_three_losses_bedwars']
            return threes_losses
        except KeyError:
            return 0

    async def get_fours_losses(self):
        try:
            fours_losses = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['four_four_losses_bedwars']
            return fours_losses
        except KeyError:
            return 0

    async def get_four_v_four_losses(self):
        try:
            four_v_four_losses = core.minecraft.hypixel.request.player_json['player']['stats']['Bedwars']['two_four_losses_bedwars']
            return four_v_four_losses
        except KeyError:
            return 0

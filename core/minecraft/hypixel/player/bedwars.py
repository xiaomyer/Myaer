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

class Bedwars():
    def __init__(self):
        self.hypixel = core.minecraft.hypixel.request.HypixelAPI()

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

    async def get_stats(self, player):
        try:
            player_json = await self.hypixel.send_player_request_uuid(player)
        except:
            raise NameError("No Hypixel stats")
            return
        player_stats = {
            "star" : player_json.get("player", {}).get("achievements", {}).get("bedwars_level", 0),
            "coins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("coins_bedwars", 0),
            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("games_played_bedwars", 0),
            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("beds_broken_bedwars", 0),
            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("beds_lost_bedwars", 0),
            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("final_kills_bedwars", 0),
            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("final_deaths_bedwars", 0),
            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("wins_bedwars", 0),
            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("losses_bedwars", 0),
            "solo" : {
                "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_games_played_bedwars", 0),
                "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_beds_broken_bedwars", 0),
                "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_beds_lost_bedwars", 0),
                "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_final_kills_bedwars", 0),
                "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_final_deaths_bedwars", 0),
                "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_wins_bedwars", 0),
                "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_losses_bedwars", 0),
            },
            "doubles" : {
                "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_games_played_bedwars", 0),
                "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_beds_broken_bedwars", 0),
                "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_beds_lost_bedwars", 0),
                "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_final_kills_bedwars", 0),
                "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_final_deaths_bedwars", 0),
                "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_wins_bedwars", 0),
                "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_losses_bedwars", 0),
            },
            "threes" : {
                "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_games_played_bedwars", 0),
                "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_beds_broken_bedwars", 0),
                "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_beds_lost_bedwars", 0),
                "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_final_kills_bedwars", 0),
                "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_final_deaths_bedwars", 0),
                "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_wins_bedwars", 0),
                "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_losses_bedwars", 0),
            },
            "fours" : {
                "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_games_played_bedwars", 0),
                "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_beds_broken_bedwars", 0),
                "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_beds_lost_bedwars", 0),
                "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_final_kills_bedwars", 0),
                "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_final_deaths_bedwars", 0),
                "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_wins_bedwars", 0),
                "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_losses_bedwars", 0),
            },
            "four_v_four" : {
                "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_games_played_bedwars", 0),
                "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_beds_broken_bedwars", 0),
                "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_beds_lost_bedwars", 0),
                "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_final_kills_bedwars", 0),
                "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_final_deaths_bedwars", 0),
                "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_wins_bedwars", 0),
                "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_losses_bedwars", 0),
            },
        }
        return player_stats

    async def get_prestige_data(self, star):
        star_rounded = star // 100 # // is floor division, basically math.floor(await self.get_star() / 100)
        star_rounded = star_rounded if star_rounded < 10 else 10 # if greater than 10, set to ten
        return {"prestige": prestiges[star_rounded], "prestige_color": prestige_colors[prestiges[star_rounded]]} # sometimes my genius, it"s...it"s almost frightnening

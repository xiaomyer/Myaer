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
from core.minecraft.hypixel.request import HypixelAPI
from core.minecraft.hypixel.static import HypixelStatic
import math

class Player():
    def __init__(self):
        self.hypixel = HypixelAPI()
        self.hypixel_static = HypixelStatic()

    async def get_player(self, player):
        try:
            player_json = await self.hypixel.send_player_request_uuid(player)
        except:
            raise NameError("No Hypixel stats")
            return
        player = {
            "name" : player_json.get("player", {}).get("displayname", ""),
            "bedwars" : {
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
                }
            },
            "skywars" : {
                "star" : math.trunc((await self.hypixel_static.get_skywars_star_from_experience((player_json.get("player", {}).get("stats", {}).get("SkyWars", {}).get("skywars_experience", 0))))),
                "coins" : player_json.get("player", {}).get("stats", {}).get("SkyWars", {}).get("coins", 0),
                "tokens" : player_json.get("player", {}).get("stats", {}).get("SkyWars", {}).get("cosmetic_tokens", 0),
                "souls" : player_json.get("player", {}).get("stats", {}).get("SkyWars", {}).get("souls", 0),
                "kills" : player_json.get("player", {}).get("stats", {}).get("SkyWars", {}).get("kills", 0),
                "deaths" : player_json.get("player", {}).get("stats", {}).get("SkyWars", {}).get("deaths", 0),
                "wins" : player_json.get("player", {}).get("stats", {}).get("SkyWars", {}).get("wins", 0),
                "losses" : player_json.get("player", {}).get("stats", {}).get("SkyWars", {}).get("losses", 0),
                "games_played" : player_json.get("player", {}).get("stats", {}).get("SkyWars", {}).get("games_played_skywars", 0)
            }
        }
        return player

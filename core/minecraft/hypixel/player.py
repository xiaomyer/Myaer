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
                "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("kills_bedwars", 0),
                "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("deaths_bedwars", 0),
                "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("final_kills_bedwars", 0),
                "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("final_deaths_bedwars", 0),
                "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("wins_bedwars", 0),
                "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("losses_bedwars", 0),
                "solo" : {
                    "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_games_played_bedwars", 0),
                    "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_beds_broken_bedwars", 0),
                    "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_beds_lost_bedwars", 0),
                    "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_kills_bedwars", 0),
                    "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_deaths_bedwars", 0),
                    "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_final_kills_bedwars", 0),
                    "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_final_deaths_bedwars", 0),
                    "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_wins_bedwars", 0),
                    "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_losses_bedwars", 0),
                },
                "doubles" : {
                    "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_games_played_bedwars", 0),
                    "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_beds_broken_bedwars", 0),
                    "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_beds_lost_bedwars", 0),
                    "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_kills_bedwars", 0),
                    "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_deaths_bedwars", 0),
                    "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_final_kills_bedwars", 0),
                    "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_final_deaths_bedwars", 0),
                    "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_wins_bedwars", 0),
                    "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_losses_bedwars", 0),
                },
                "threes" : {
                    "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_games_played_bedwars", 0),
                    "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_beds_broken_bedwars", 0),
                    "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_beds_lost_bedwars", 0),
                    "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_kills_bedwars", 0),
                    "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_deaths_bedwars", 0),
                    "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_final_kills_bedwars", 0),
                    "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_final_deaths_bedwars", 0),
                    "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_wins_bedwars", 0),
                    "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_three_losses_bedwars", 0),
                },
                "fours" : {
                    "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_games_played_bedwars", 0),
                    "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_beds_broken_bedwars", 0),
                    "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_beds_lost_bedwars", 0),
                    "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_kills_bedwars", 0),
                    "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_deaths_bedwars", 0),
                    "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_final_kills_bedwars", 0),
                    "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_final_deaths_bedwars", 0),
                    "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_wins_bedwars", 0),
                    "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_losses_bedwars", 0),
                },
                "four_v_four" : {
                    "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_games_played_bedwars", 0),
                    "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_beds_broken_bedwars", 0),
                    "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_beds_lost_bedwars", 0),
                    "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_kills_bedwars", 0),
                    "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_deaths_bedwars", 0),
                    "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_final_kills_bedwars", 0),
                    "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_final_deaths_bedwars", 0),
                    "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_wins_bedwars", 0),
                    "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("two_four_losses_bedwars", 0),
                },
                "dreams" : {
                    "armed" : {
                        "doubles" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_armed_diamond_resources_collected_bedwars", 0),
                            }
                        },
                        "fours" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_armed_diamond_resources_collected_bedwars", 0),
                            }
                        }
                    },
                    "castle" : {
                        "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_games_played_bedwars", 0),
                        "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_beds_broken_bedwars", 0),
                        "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_beds_lost_bedwars", 0),
                        "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_kills_bedwars", 0),
                        "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_void_kills_bedwars", 0),
                        "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_deaths_bedwars", 0),
                        "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_void_deaths", 0),
                        "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_final_kills_bedwars", 0),
                        "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_final_deaths_bedwars", 0),
                        "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_wins_bedwars", 0),
                        "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_losses_bedwars", 0),
                        "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_winstreak_bedwars", 0),
                        "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle__items_purchased_bedwars", 0),
                        "resources_collected" : {
                            "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_resources_collected_bedwars", 0),
                            "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_iron_resources_collected_bedwars", 0),
                            "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_gold_resources_collected_bedwars", 0),
                            "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_emerald_resources_collected_bedwars", 0),
                            "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("castle_diamond_resources_collected_bedwars", 0),
                        }
                    },
                    "lucky_blocks" : {
                        "doubles" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_lucky_diamond_resources_collected_bedwars", 0),
                            }
                        },
                        "fours" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_lucky_diamond_resources_collected_bedwars", 0),
                            }
                        }
                    },
                    "rush" : {
                        "solo" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_deaths_bedwars", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_final_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_void_deaths", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_rush_diamond_resources_collected_bedwars", 0),
                            }
                        },
                        "doubles" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_rush_diamond_resources_collected_bedwars", 0),
                            }
                        },
                        "fours" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_rush_diamond_resources_collected_bedwars", 0),
                            }
                        }
                    },
                    "ultimate" : {
                        "solo" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_one_ultimate_diamond_resources_collected_bedwars", 0),
                            }
                        },
                        "doubles" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_ultimate_diamond_resources_collected_bedwars", 0),
                            }
                        },
                        "fours" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_ultimate_diamond_resources_collected_bedwars", 0),
                            }
                        }
                    },
                    "voidless" : {
                        "doubles" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("eight_two_voidless_diamond_resources_collected_bedwars", 0),
                            }
                        },
                        "fours" : {
                            "games_played" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_games_played_bedwars", 0),
                            "beds_broken" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_beds_broken_bedwars", 0),
                            "beds_lost" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_beds_lost_bedwars", 0),
                            "kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_kills_bedwars", 0),
                            "void_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_void_kills_bedwars", 0),
                            "deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_deaths_bedwars", 0),
                            "void_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_void_deaths", 0),
                            "final_kills" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_final_kills_bedwars", 0),
                            "final_deaths" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_final_deaths_bedwars", 0),
                            "wins" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_wins_bedwars", 0),
                            "losses" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_losses_bedwars", 0),
                            "winstreak" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_winstreak_bedwars", 0),
                            "items_purchased" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless__items_purchased_bedwars", 0),
                            "resources_collected" : {
                                "all" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_resources_collected_bedwars", 0),
                                "iron" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_iron_resources_collected_bedwars", 0),
                                "gold" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_gold_resources_collected_bedwars", 0),
                                "emeralds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_emerald_resources_collected_bedwars", 0),
                                "diamonds" : player_json.get("player", {}).get("stats", {}).get("Bedwars", {}).get("four_four_voidless_diamond_resources_collected_bedwars", 0),
                            }
                        }
                    }
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

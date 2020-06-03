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
import re

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
	"Rainbow",
	"Rainbow" # this is for the skywars bit, since rainbow prestige has twice the amount of levels as the others, we need it twice
]

ranks = {
	"NONE" : None,
	"VIP_PLUS" : "VIP+",
	"MVP_PLUS" : "MVP+",
	"SUPERSTAR" : "MVP++",
	"YOUTUBER" : "YOUTUBE",
	"MODERATOR" : "MOD",
}

rank_colors = {
	"VIP" : "55FF55",
	"VIP+" : "55FF55",
	"MVP" : "55FFFF",
	"MVP+" : "55FFFF",
	"MVP++" : "FFAA00",
	"YOUTUBE" : "FF5555",
	"PIG+++" : "FF69DC",
	"BUILD TEAM" : "00AAAA",
	"EVENTS" : "FFAA00",
	"HELPER" : "5555FF",
	"MOD" : "00AA00",
	"ADMIN" : "AA0000",
	"SLOTH" : "AA0000",
	"OWNER" : "AA0000",
	None : "607D8B"
}

hypixel_icons = { # Hypixel icons
	"Main" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/main.png",
	"Arcade" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/arcade.png",
	"Bedwars" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/bedwars.png",
	"BlitzSurvivalGames" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/blitz_survival_games.png",
	"BuildBattle" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/build_battle.png",
	"Classic" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/classic.png",
	"CrazyWalls" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/crazy_walls.png",
	"CVC" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/cvc.png",
	"Duels" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/duels.png",
	"Housing" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/housing.png",
	"MegaWalls" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/mega_walls.png",
	"MurderMystery" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/murder_mystery.png",
	"Pit" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/pit.png",
	"Prototype" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/prototype.png",
	"Skyblock" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/skyblock.png",
	"Skywars" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/skywars.png",
	"SmashHeroes" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/",
	"TNT" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/tnt.png",
	"UHC" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/uhc_champions", # UHC Champions is the only thing resembling UHC on Hypixel
	"Warlords" : "https://raw.githubusercontent.com/MyerFire/Myaer/master/core/minecraft/hypixel/static/warlords.png"
}


async def get_network_level_data(experience):
	level = (math.sqrt(experience + 15312.5) - 88.38834764831843) / 35.35533905932738 # formula that i don't understand, something to do with square roots - thank you @littlemissantivirus
	level_data = {
		"level" : math.trunc(level),
		"percentage" : round((level - math.trunc(level)) * 100, 2)
	}
	return level_data


async def get_rank_data(self, rank, prefix_raw, monthly_package_rank, new_package_rank, package_rank): # complicated because returning the formatted rank name
	rank_data = {
		"prefix": None,
		"top_rank": None,
		"rank": None
	}
	if prefix_raw:
		prefix = re.sub(r"§.", "", prefix_raw)[1:-1] # prefixes all start and end with brackets, and have minecraft color codes, this is to remove color codes and brackets
		rank_data["prefix"] = ranks.get(prefix, prefix)
		rank_data["color"] = rank_colors[rank_data["prefix"]]

	if rank:
		rank_data["top_rank"] = ranks.get(rank, rank)
		rank_data["color"] = rank_colors[rank_data["top_rank"]]

	if monthly_package_rank:
		rank_data["rank"] = ranks.get(monthly_package_rank, monthly_package_rank)
		rank_data["color"] = rank_colors[rank_data["rank"]]
	else:
		if new_package_rank:
			rank_data["rank"] = ranks.get(new_package_rank, new_package_rank)
		else:
			rank_data["rank"] = ranks.get(package_rank, package_rank)
		rank_data["color"] = rank_colors[rank_data["rank"]] # there is probably a better way to do this, but it's probably longer or unnecessarily complicated
	return rank_data

async def get_ratio(positive_stat, negative_stat):
	try:
		ratio = positive_stat / negative_stat
		return round(ratio, 2)
	except ZeroDivisionError:
		return float("inf") if positive_stat > 0 else 0


async def get_increase_stat(positive_stat, negative_stat, increase):
	# positive_stat is a "good" stat like final_kills
	# negative_stat is a "bad" stat like final_deaths
	# increase is the amount the positive_stat to negative_stat ratio needs to increase
	try:
		stat = positive_stat / negative_stat
		needed = (stat + increase) * negative_stat - positive_stat
		return round(needed)
	except ZeroDivisionError:
		return float("inf") if positive_stat > 0 else 0


async def get_bedwars_prestige_data(star):
	star_rounded = star // 100 # // is floor division, basically math.floor(await self.get_star() / 100)
	if star_rounded > 10:
		prestige = "Rainbow"
	else:
		prestige = prestiges[star_rounded]
	return {
		"prestige": prestige,
		"prestige_color": prestige_colors[prestige]
	} # based on order of prestiges and prestige colors


async def get_skywars_prestige_data(star):
	star_rounded = star // 5
	if star_rounded > 11:
		prestige = "Mystic"
	else:
		prestige = prestiges[star_rounded] # MY BRAIN IS SO LARGE
	return {
		"prestige": prestige,
		"prestige_color": prestige_colors["Rainbow" if prestige == "Mystic" else prestige] # mystic uses rainbow color
	}


async def get_skywars_star_from_experience(experience): # another formula that I don't understand, thanks to @GamingGeeek and @littlemissantivirus
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

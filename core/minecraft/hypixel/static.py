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

import discord
import math
import core.minecraft.hypixel.player
import re
import core.minecraft.verification.verification

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

ranks = {
	"NONE" : None,
	"VIP" : "VIP",
	"VIP_PLUS" : "VIP+",
	"MVP" : "MVP",
	"MVP_PLUS" : "MVP+",
	"SUPERSTAR" : "MVP++",
	"YOUTUBER" : "YOUTUBE",
	"PIG+++" : "PIG+++",
	"BUILD TEAM" : "BUILD TEAM",
	"HELPER" : "HELPER",
	"MODERATOR" : "MOD",
	"ADMIN" : "ADMIN",
	"SLOTH" : "SLOTH",
	"OWNER" : "OWNER"
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

async def get_guild_level_data(experience): # credit for original formula to @Sk1er, translated into Kotlin by @littlemissantivirus, then translated into Python by @SirNapkin1334
	experienceBelow14 = [100000, 150000, 250000, 500000, 750000, 1000000, 1250000, 1500000, 2000000, 2500000, 2500000, 2500000, 2500000, 2500000]
	c = 0.0
	for it in experienceBelow14:
		if (it > experience):
			level = c + round(experience / it * 100.0) / 100.0
		experience -= it
		c+=1

		increment = 3000000

	while experience > increment:
		c+=1
		experience-=increment

	level = c + (round(experience / increment * 100.0) / 100.0)
	level_data = {
		"level" : math.trunc(level),
		"percentage" : round((level - math.trunc(level)) * 100, 2)
	}
	return level_data

async def get_rank_data(rank, prefix_raw, monthly_package_rank, new_package_rank, package_rank): # complicated because returning the formatted rank name
	formatted_rank = None
	if prefix_raw:
		prefix = re.sub(r"§.", "", prefix_raw)[1:-1] # prefixes all start and end with brackets, and have minecraft color codes, this is to remove color codes and brackets
		formatted_rank = ranks.get(prefix, prefix)

	elif rank and not formatted_rank:
		formatted_rank = ranks.get(rank, rank)

	elif (monthly_package_rank and monthly_package_rank != "NONE") and not formatted_rank: # WHY DOES IT EXIST IF IT'S NONE HYPIXEL WHY
		formatted_rank = ranks.get(monthly_package_rank, monthly_package_rank)

	elif new_package_rank and not formatted_rank:
		formatted_rank = ranks.get(new_package_rank, new_package_rank)

	elif package_rank and not formatted_rank:
		formatted_rank = ranks.get(package_rank, package_rank)

	rank_data = {
		"rank" : formatted_rank,
		"color" : rank_colors[formatted_rank]
	}
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
	star_rounded = star_rounded if star_rounded < 10 else 10 # if greater than 10, set to ten
	return {
				"prestige": prestiges[star_rounded],
				"prestige_color": prestige_colors[prestiges[star_rounded]]
	} # based on order of prestiges and prestige colors

async def get_skywars_prestige_data(star):
	if star in range(0, 5):
		prestige = "Stone"
		prestige_color = prestige_colors[prestige]
	elif star in range(5, 10):
		prestige = "Iron"
		prestige_color = prestige_colors[prestige]
	elif star in range(10, 15):
		prestige = "Gold"
		prestige_color = prestige_colors[prestige]
	elif star in range(15, 20):
		prestige = "Diamond"
		prestige_color = prestige_colors[prestige]
	elif star in range(20, 25):
		prestige = "Emerald"
		prestige_color = prestige_colors[prestige]
	elif star in range(25, 30):
		prestige = "Sapphire"
		prestige_color = prestige_colors[prestige]
	elif star in range(30, 35):
		prestige = "Ruby"
		prestige_color = prestige_colors[prestige]
	elif star in range(35, 40):
		prestige = "Crystal"
		prestige_color = prestige_colors[prestige]
	elif star in range(40, 45):
		prestige = "Opal"
		prestige_color = prestige_colors[prestige]
	elif star in range(45, 50):
		prestige = "Amethyst"
		prestige_color = prestige_colors[prestige]
	elif star in range(50, 60):
		prestige = "Rainbow"
		prestige_color = prestige_colors[prestige]
	else:
		prestige = "Mystic"
		prestige_color = prestige_colors["Rainbow"] # Mystic and Rainbow use the same color

	prestige_data = {
		"prestige" : prestige,
		"prestige_color" : prestige_color
	}
	return prestige_data

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

async def name_handler(ctx, args, *, get_guild: bool = False):
	if len(args):
		try:
			player_data = await core.minecraft.verification.verification.parse_input(ctx, args[0])
		except AttributeError:
			member_not_verified = discord.Embed(
				name = "Member not verified",
				description = f"{args[0]} is not verified. Tell them to do `/mc verify <their-minecraft-ign>`",
				color = ctx.author.color
			)
			await ctx.send(embed = member_not_verified)
			return
		except NameError:
			nameerror_embed = discord.Embed(
				name = "Invalid input",
				description = f"\"{args[0]}\" is not a valid username or UUID.",
				color = ctx.author.color
			)
			await ctx.send(embed = nameerror_embed)
			return
	else:
		player_data = await core.minecraft.verification.verification.database_lookup(ctx.author.id)
		if player_data is None:
			unverified_embed = discord.Embed(
				name = "Not verified",
				description = "You have to verify with `/mc verify <minecraft-ign>` first.",
				color = ctx.author.color
			)
			await ctx.send(embed = unverified_embed)
			return
	try:
		player_json = await core.minecraft.hypixel.player.get_player_data(player_data["minecraft_uuid"], get_guild = get_guild)
	except NameError:
		nameerror_embed = discord.Embed(
			name = "Invalid input",
			description = f"\"{player_data['player_formatted_name']}\" does not seem to have Hypixel stats.",
			color = ctx.author.color
		)
		await ctx.send(embed = nameerror_embed)
		return
	player_info = {
		"player_data" : player_data,
		"player_json" : player_json
	}
	return player_info

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

import core.caches.friends
import ratelimit
import core.minecraft.request
import core.minecraft.hypixel.request
import core.minecraft.hypixel.static.static

games = {}

async def get_status(uuid):
	try:
		status_json = (await core.minecraft.hypixel.request.get_status_by_uuid(uuid))
	except NameError:
		raise NameError("Invalid UUID")
	except ratelimit.RateLimitException:
		raise OverflowError # idk how to make custom exceptions so this is close enough

	status = {
		"online" : status_json.get("session", {}).get("online", False),
		"session" : await game_parser(status_json.get("session", {}).get("gameType", ""), status_json.get("session", {}).get("mode", "")) if status_json.get("session", {}).get("online", False) else None
	}
	return status

async def game_parser(raw_game_type, raw_game_mode):
	global games
	if not games:
		games = await core.minecraft.hypixel.request.get_games_connor_linfoot()

	game_formatted_name = ""
	game_formatted_mode = ""
	for game_type in games:
		if not game_formatted_name:
			if raw_game_type == game_type["key"]:
				game_formatted_name = game_type["name"]
		if not game_formatted_mode and bool(game_type.get("modes", None)):
			if raw_game_mode != "LOBBY":
				for game_mode in game_type["modes"]:
					if not game_formatted_mode:
						if raw_game_mode == game_mode["key"]:
							game_formatted_mode = game_mode["name"]
			else:
				game_formatted_mode = "Lobby"
	game_data = {
		"game" : game_formatted_name,
		"instance" : game_formatted_mode,
		"formatted" : f"is currently in a {game_formatted_name} {game_formatted_mode} game" if game_formatted_mode != "Lobby" else f"is currently in a {game_formatted_name} {game_formatted_mode}"
	}
	return game_data

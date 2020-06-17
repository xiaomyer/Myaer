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
import core.minecraft.request
import core.minecraft.hypixel.request
import core.minecraft.hypixel.static

async def get_friends(uuid):
	friends_cache = await core.caches.friends.find_friends_data(uuid)
	if friends_cache:
		return friends_cache
	try:
		friends_json = (await core.minecraft.hypixel.request.get_friends_by_uuid(uuid))
	except:
		raise NameError("No friends")
	friends = []
	for player in friends_json["records"]:
		player_uuid = player["uuidSender"] if player["uuidSender"] != uuid else player["uuidReceiver"]
		player_profile = await core.minecraft.hypixel.player.get_player_data(player_uuid) if player_uuid != core.minecraft.hypixel.static.master_control else {"name" : "MasterControl", "rank_data" : {"rank" : "[MCP]", "color" : "AA0000"}} # technoblade has the account MasterControl friended, and that account is a hypixel alt that isn't in the api
		friends.append(player_profile)
	await core.caches.friends.save_friends_data(uuid, friends)
	return friends

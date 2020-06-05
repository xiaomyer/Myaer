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

from tinydb import TinyDB, Query, where

async def get_prefix(guild_id):
	db = TinyDB("/home/myerfire/Myaer/Myaer/prefixes.json")
	try:
		return db.search(where("guild_id") == guild_id)
	except:
		return None

async def set_prefix(guild_id, prefix):
	db = TinyDB("/home/myerfire/Myaer/Myaer/prefixes.json")
	Prefixes = Query()
	if db.search(where("guild_id") == guild_id):
		db.update({"prefix" : prefix}, Prefixes.guild_id == guild_id)
	elif db.search(where("guild_id") == guild_id):
		db.remove(Prefixes.guild_id == guild_id)
		db.insert({"guild_id" : guild_id, "prefix" : prefix})
	else:
		db.insert({"guild_id" : guild_id, "prefix" : prefix})

async def reset_prefix(guild_id):
	db = TinyDB("/home/myerfire/Myaer/Myaer/prefixes.json")
	Prefixes = Query()
	if db.search(where("guild_id") == guild_id):
		saved_data = db.search(where("guild_id") == guild_id)
		db.remove(Prefixes.guild_id == guild_id)
		return saved_data
	else:
		raise NameError("Prefix was not set")

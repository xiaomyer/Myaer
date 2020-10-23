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

import core.minecraft.hypixel.request
import core.minecraft.hypixel.static

tag_colors = {
    "DARK_GREEN": "00AA00",
    "YELLOW": "FFFF55"
}


async def get_guild_data(uuid):
    try:
        guild_json = (await core.minecraft.hypixel.request.get_guild_by_uuid(uuid))
    except NameError:
        raise NameError("Not in a guild")
    guild = {
        "name": guild_json.get("guild", {}).get("name", ""),
        "level_data": (await core.minecraft.hypixel.static.get_guild_level_data(
            (guild_json.get("guild", {}).get("exp", 0)))),
        "color": tag_colors.get((guild_json.get("guild", {}).get("tagColor", "")), None),
        "tag": guild_json.get("guild", {}).get("tag", "")
    }
    return guild

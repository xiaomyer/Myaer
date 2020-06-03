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

async def get_leaderboards():
    leaderboards_json = await core.minecraft.hypixel.request.send_leaderboard_request()
    leaderboards = {
        "bedwars" : {
            "level" : leaderboards_json["leaderboards"]["BEDWARS"][0]["leaders"],
            "wins" : {
                "overall" : leaderboards_json["leaderboards"]["BEDWARS"][1]["leaders"],
                "weekly" : leaderboards_json["leaderboards"]["BEDWARS"][2]["leaders"]
            },
            "finals" : {
                "overall" : leaderboards_json["leaderboards"]["BEDWARS"][3]["leaders"],
                "weekly" : leaderboards_json["leaderboards"]["BEDWARS"][4]["leaders"]
            }
        }
    }
    return leaderboards

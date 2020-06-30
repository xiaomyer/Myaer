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


arrow_bullet_point = "➤"
star = "✫"
stats_needed_disclaimer = "Note - The amount needed for stat increase assumes that no negative stats are taken (no final deaths, no losses, etc)"
wrist_spasm_disclaimer = "Specific to Wrist Spasm"


async def get_role_mentions(roles) -> list:
    role_names = []
    for role in reversed(roles):  # discord roles attribute of a guild returns roles from lowest to highest
        if role.name != "@everyone":  # @everyone is a default role that doesn't have to be shown
            role_names.append(f"<@&{role.id}>")
    return role_names


async def get_role_mentions_string(roles: list) -> str:
    if bool(roles):
        times = 0
        while len(", ".join(roles)) > 1024:
            del roles[-1]
            times += 1
        return f"{', '.join(roles)}" if not bool(times) else f"{', '.join(roles)} (and {times} more)"
    else:
        return "No Roles"
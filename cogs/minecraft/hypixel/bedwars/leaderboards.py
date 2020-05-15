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

from core.minecraft.hypixel.leaderboards.bedwars import BedwarsLeaderboards
from discord.ext import commands
import discord
import core.discord.markdown
import core.minecraft.hypixel.request

class BedwarsLeaderboardsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.markdown = core.discord.markdown.Markdown()
        self.request = core.minecraft.hypixel.request.Request()
        self.leaderboards = core.minecraft.hypixel.leaderboards.bedwars.BedwarsLeaderboards()

    @commands.command(name = "lbbw")
    async def get_level_leaderboard(self, ctx):
        await self.request.send_leaderboard_request()
        level_leaderboard_embed = discord.Embed(
            name = "Levels Leaderboard",
            color = ctx.author.color
        )
        level_leaderboard_embed.add_field(
            name = "1st",
            value = f"{(await self.leaderboards.get_levels())[0]}"
        )
        await ctx.send(embed = level_leaderboard_embed)

def setup(bot):
    bot.add_cog(BedwarsLeaderboardsCommands(bot))
    print("Reloaded cogs.minecraft.hypixel.bedwars.leaderboards")

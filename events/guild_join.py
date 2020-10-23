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
from discord.ext import commands

import core.minecraft.verification


class OnGuildJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_join_embed = discord.Embed(
            name="Joined guild",
            title=f"**Joined Guild {discord.utils.escape_markdown(f'{guild.name}')}**"
        )
        guild_join_embed.add_field(
            name=f"__**{core.static.arrow_bullet_point} ID**__",
            value=f"{guild.id}"
        )
        guild_join_embed.add_field(
            name=f"__**{core.static.arrow_bullet_point} Members**__",
            value=f"{(len(guild.members)):,d}"
        )
        guild_join_embed.set_thumbnail(
            url=str(guild.icon_url_as(static_format="png", size=2048))
        )
        await self.bot.guilds_log_channel.send(embed=guild_join_embed)


def setup(bot):
    bot.add_cog(OnGuildJoin(bot))
    print("Reloaded events.guild_join")

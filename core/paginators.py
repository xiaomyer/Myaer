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
from discord.ext import menus


class MinecraftNameHistory(menus.ListPageSource):
    def __init__(self, data, ctx, player_data):
        self.ctx = ctx
        self.player_data = player_data
        super().__init__(data, per_page=15)

    async def format_page(self, menu, entries):
        joined = "\n".join(entries)
        page_embed = discord.Embed(
            title=self.player_data["player_formatted_name"],
            description=f"```{joined}```",
            color=self.ctx.author.color,
            timestamp=self.ctx.message.created_at
        )
        return page_embed


class MinecraftHypixelFriends(menus.ListPageSource):
    def __init__(self, data, ctx, player_json):
        self.ctx = ctx
        self.player_json = player_json
        self.data = data
        super().__init__(data, per_page=15)

    async def format_page(self, menu, entries):
        joined = "\n".join(entries)
        page_embed = discord.Embed(
            title=f"{self.player_json['name']}'s Friends List ({len(self.data)} friends)",
            description=f"```{joined}```",
            color=int((self.player_json["rank_data"])["color"], 16),  # 16 - hex value
            timestamp=self.ctx.message.created_at
        )
        return page_embed


class Analytics_(menus.ListPageSource):
    def __init__(self, data, ctx, total):
        self.ctx = ctx
        self.total = total
        super().__init__(data, per_page=15)

    async def format_page(self, menu, entries):
        joined = "\n".join(entries)
        page_embed = discord.Embed(
            title=f"Command Analytics (Total of {self.total})",
            description=f"```{joined}```",
            color=self.ctx.author.color,
            timestamp=self.ctx.message.created_at,
        ).set_footer(
            text="Started tracking on September 9th, 2020"
        )
        return page_embed


class SessionAnalytics(menus.ListPageSource):
    def __init__(self, data, ctx, total):
        self.ctx = ctx
        self.total = total
        super().__init__(data, per_page=15)

    async def format_page(self, menu, entries):
        joined = "\n".join(entries)
        page_embed = discord.Embed(
            title=f"Session Command Analytics (Total of {self.total})",
            description=f"```{joined}```",
            color=self.ctx.author.color,
            timestamp=self.ctx.message.created_at,
        )
        return page_embed

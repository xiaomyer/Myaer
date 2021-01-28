"""
MIT License

Copyright (c) 2020 Myer

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

import humanfriendly
import discord
from discord.ext import commands, menus


class LastFM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["fm"])
    async def lastfm(self, ctx):
        return

    @lastfm.command()
    async def set(self, ctx, username):
        user = await ctx.bot.lastfm.client.user.get_info(username)
        ctx.bot.data.users.set(ctx.author.id, "lastfm", user.name)
        return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Verified your last.fm account as `{user.name}`"))

    @lastfm.command()
    async def recent(self, ctx, username=None):
        username = await ctx.bot.lastfm.get_username(ctx=ctx, username=username)
        tracks = await ctx.bot.lastfm.client.user.get_recent_tracks(user=username)
        names = [f"{track.artist.name} - " 
                 f"{track.name} - "
                 f"{'now playing' if track.playing else f'{humanfriendly.format_timespan(ctx.bot.static.time() - track.played)} ago'}"
                 for track in tracks.items]
        await menus.MenuPages(source=RecentTracksPaginator(names, ctx, username),
                              clear_reactions_after=True
                              ).start(ctx)

    @lastfm.command(aliases=["np"])
    async def now(self, ctx, username=None):
        username = await ctx.bot.lastfm.get_username(ctx=ctx, username=username)
        tracks = await ctx.bot.lastfm.client.user.get_recent_tracks(user=username)
        track = tracks.items[0] if tracks.items[0].playing else None
        if track:
            await ctx.send(embed=discord.Embed(
                title=f"{track.artist.name} - {track.name}",
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            ).set_image(
                url=track.image[-1].url
            ).set_footer(
                text="Now playing"
            ))
        else:
            await ctx.send(embed=ctx.bot.static.embed(ctx, description="Not currently playing anything"))


class RecentTracksPaginator(menus.ListPageSource):
    def __init__(self, data, ctx, username):
        self.ctx = ctx
        self.username = username
        super().__init__(data, per_page=15)

    async def format_page(self, menu, entries):
        joined = "\n".join(entries)
        return discord.Embed(
            title=f"{self.username}'s Recent Tracks",
            description=f"```{joined}```",
            color=self.ctx.author.color,
            timestamp=self.ctx.message.created_at
        )


def setup(bot):
    bot.add_cog(LastFM(bot))
    print("Reloaded cogs.lastfm")

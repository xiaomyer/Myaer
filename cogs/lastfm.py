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

import io

import aiohttp
import discord
import humanfriendly
import lastfmpy
from PIL import Image
from bs4 import BeautifulSoup
from discord.ext import commands, menus


class LastFM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_default = 900
        self.image_default_size = 900, 900
        self.url_cache = {}
        self.image_cache = {}

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
        recent = await ctx.bot.lastfm.client.user.get_recent_tracks(user=username)
        tracks = [f"`{track.artist.name} - "
                  f"{track.name} | "
                  f"{'(now playing)' if track.playing else f'({humanfriendly.format_timespan(ctx.bot.static.time() - track.played, max_units=2)} ago)'}`"
                  for track in recent.items]
        await menus.MenuPages(
            source=ctx.bot.static.paginators.regular(tracks, ctx, f"{username}'s Recent Tracks", "Recently played"),
            clear_reactions_after=True
        ).start(ctx)

    @lastfm.command(aliases=["np"])
    async def now(self, ctx, username=None):
        username = await ctx.bot.lastfm.get_username(ctx=ctx, username=username)
        tracks = await ctx.bot.lastfm.client.user.get_recent_tracks(user=username)
        track = tracks.items[0] if tracks.items[0].playing else None
        if track:
            track_full = await self.try_get_track(artist=track.artist.name, track=track.name, username=username)
            embed = discord.Embed(
                title=f"{track.artist.name} - {track.name}",
                color=ctx.author.color,
                timestamp=ctx.message.created_at,
            ).set_image(
                url=track.image[-1].url
            ).set_footer(
                text="Now playing"
            )
            if bool(track_full):
                embed.description = f"{track_full.stats.userplaycount} plays"
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=ctx.bot.static.embed(ctx, description="Not currently playing anything"))

    @lastfm.command(aliases=["servernp"])
    async def servernow(self, ctx):
        await ctx.trigger_typing()
        usernames = []
        for member in ctx.guild.members:
            if lastfm := ctx.bot.data.users.get(member.id).lastfm:
                usernames.append((member, lastfm))
        tracks = []
        for member, user in usernames:
            recent = await ctx.bot.lastfm.client.user.get_recent_tracks(user=user)
            now = recent.items[0] if recent.items[0].playing else None
            if bool(now):
                now_full = await self.try_get_track(artist=now.artist.name, track=now.name, username=user)
                string = f"{member.mention}: `{now.artist.name} - {now.name}{f' ({now_full.stats.userplaycount} plays)`' if bool(now_full) else '`'}"
                tracks.append(string)
        if not tracks:
            return await ctx.send(embed=ctx.bot.static.embed(ctx, f"No one in {ctx.guild} is listening to anything"))
        await menus.MenuPages(source=ctx.bot.static.paginators.regular(tracks, ctx, f"{ctx.guild}'s Now Playing",
                                                                       "Server now playing")).start(
            ctx)

    @lastfm.command()
    async def chart(self, ctx, first=None, second=3):
        # first and second argument, if a number is in the first argument then take it as the per value
        # otherwise, take first argument as username and second argument as the per value
        await ctx.trigger_typing()
        if bool(first) and first.isdigit():
            second = int(first)
            first = None
        first = await ctx.bot.lastfm.get_username(ctx=ctx, username=first)
        chart = await ctx.bot.lastfm.client.user.get_weekly_album_chart(first)
        images = await self.get_image_pil(await self.scrape_images(chart.items[:second ** 2]))
        # per ** 2 is the maximum amount of images that could be displayed
        final = self.image_to_bytes(self.merge_images(images, per=second))
        await ctx.send(file=discord.File(final, filename="chart.png"))

    async def try_get_track(self, artist=None, track=None, username=None):
        try:
            return await self.bot.lastfm.client.track.get_info(track=track, artist=artist, username=username)
        except lastfmpy.InvalidInputError:
            return

    async def scrape_images(self, albums: list) -> list:
        urls = []
        async with aiohttp.ClientSession() as session:
            for album in albums:
                if url := self.url_cache.get(album.url):
                    urls.append(url)
                else:
                    html = await session.get(album.url)
                    html = BeautifulSoup(await html.read(), "html.parser")
                    url = html.find("meta", property="og:image")["content"]
                    self.url_cache[album.url] = html.find("meta", property="og:image")["content"]
                    urls.append(url)
        return urls

    async def get_image_pil(self, images: list) -> list:
        files = []
        async with aiohttp.ClientSession() as session:
            for image in images:
                if file := self.image_cache.get(image):
                    files.append(file)
                else:
                    file = Image.open(io.BytesIO(await (await session.get(image)).read()))
                    files.append(file)
                    self.image_cache[image] = file
        return files

    def merge_images(self, images: list, per: int = 3) -> Image:
        final = Image.new("RGB", size=self.image_default_size)
        x = 0
        y = 0
        for image in images:
            image = image.resize((self.image_default // per, self.image_default // per))
            final.paste(image, (x, y))
            if x == self.image_default or x + self.image_default // per == self.image_default:
                x = 0
            else:
                x += self.image_default // per
                continue
            if y == self.image_default or y + self.image_default // per == self.image_default:
                y = 0
            else:
                y += self.image_default // per
        return final

    @staticmethod
    def image_to_bytes(image: Image) -> io.BytesIO:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="png")
        image_bytes.seek(0)
        return image_bytes


def setup(bot):
    bot.add_cog(LastFM(bot))
    print("Reloaded cogs.lastfm")

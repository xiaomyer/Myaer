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
import textwrap
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from discord.ext import commands, menus


class LastFM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_default = 900
        self.image_default_size = 900, 900
        self.template = Image.open("static/nowplaying.png")
        # width = 400, height = 150
        # the box on the template is 10 pixels down, 10 pixels to the right
        self.url_cache = {}
        self.image_cache = {}
        self.font = ImageFont.truetype("static/calibri.ttf", 20)
        self.font_small = ImageFont.truetype("static/calibri.ttf", 14)

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
            source=ctx.bot.static.paginators.regular(tracks, ctx, discord.Embed(
                title=f"{username}'s Recent Tracks",
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            ).set_footer(
                text="Recently played",
            )),
            clear_reactions_after=True
        ).start(ctx)

    @lastfm.command(aliases=["np"])
    async def now(self, ctx, username=None):
        username = await ctx.bot.lastfm.get_username(ctx=ctx, username=username)
        now = await ctx.bot.lastfm.client.user.get_now_playing(username)
        if now:
            now_full = await self.try_get_track(artist=now.artist.name, track=now.name, username=username)
            cover = ctx.bot.static.image_to_pil(await ctx.bot.static.get_image(now.image[-1].url))
            cover = cover.resize((129, 129))
            image = self.template.copy()
            draw = ImageDraw.Draw(image)
            image.paste(cover, (11, 11))
            if bool(now_full):
                playcount_string = f"{now_full.stats.userplaycount} plays"
                draw.text((
                    self.get_playcount_x(self.font_small, playcount_string),
                    150 - 25
                ), playcount_string, font=self.font_small)
            string = f"{now.name} ― {now.artist.name}"
            string_wrapped = [line for line in textwrap.wrap(string, 25,
                                                             break_on_hyphens=False, max_lines=6)]
            total_height = 0
            for line in string_wrapped:
                _, height = self.font.getsize(line)
                total_height += height + 6
            height, y = self.get_intial_y(total_height)
            for line in string_wrapped:
                x = self.get_x(self.font, line)
                draw.text((x, y,), line, font=self.font)
                y += self.font.size + 3
            await ctx.send(file=discord.File(ctx.bot.static.image_to_bytes(image), filename="np.png"))
        else:
            await ctx.send(embed=ctx.bot.static.embed(ctx, description="Not currently playing anything"))

    @lastfm.command(aliases=["servernp"])
    async def servernow(self, ctx):
        await ctx.trigger_typing()
        users = self.get_server_lastfm(ctx)
        tracks = []
        for member, user in users:
            now = await ctx.bot.lastfm.client.user.get_now_playing(user)
            if bool(now):
                now_full = await self.try_get_track(artist=now.artist.name, track=now.name, username=user)
                string = f"{member.mention}: `{now.artist.name} - {now.name}{f' ({now_full.stats.userplaycount} plays)`' if bool(now_full) else '`'}"
                tracks.append(string)
        if not tracks:
            return await ctx.send(embed=ctx.bot.static.embed(ctx, f"No one in {ctx.guild} is listening to anything"))
        await menus.MenuPages(source=ctx.bot.static.paginators.regular(tracks, ctx, discord.Embed(
            title=f"{ctx.guild}'s Now Playing",
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        ).set_footer(
            text="Recently played",
        ), clear_reactions_after=True
                                                                       )).start(ctx)

    @lastfm.command(aliases=["wk"])
    async def whoknows(self, ctx, *, artist=None):
        await ctx.trigger_typing()
        if not artist:
            username = await ctx.bot.lastfm.get_username(ctx=ctx)
            now = await ctx.bot.lastfm.client.user.get_now_playing(username)
            if not bool(now):
                return await ctx.send(embed=ctx.bot.static.embed(ctx, f"Not currently playing anything"))
            artist = now.artist
        else:
            artist = await ctx.bot.lastfm.client.artist.get_info(artist=artist)
        users = self.get_server_lastfm(ctx)
        knows = []
        counts = []
        for member, user in users:
            artist_full = await ctx.bot.lastfm.client.artist.get_info(artist=artist.name, username=user)
            if bool(artist_full.stats.userplaycount):
                string = f"{member.mention}: `{artist_full.name} ({artist_full.stats.userplaycount} plays)`"
                knows.append(string)
                counts.append(artist_full.stats.userplaycount)
        knows.sort(key=dict(zip(knows, counts)).get, reverse=True)
        if not knows:
            return await ctx.send(embed=ctx.bot.static.embed(ctx, f"No one in {ctx.guild} knows `{artist}`"))
        await menus.MenuPages(
            source=ctx.bot.static.paginators.regular(knows, ctx, discord.Embed(
                title=f"Who In {ctx.guild} Knows {artist}",
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            ).set_footer(
                text="Who Knows",
            ))).start(ctx)

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
        final = ctx.bot.static.image_to_bytes(self.merge_images(images, per=second))
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
        for image in images:
            if file := self.image_cache.get(image):
                files.append(file)
            else:
                file = self.bot.static.image_to_pil(await self.bot.static.get_image(image))
                files.append(file)
                self.image_cache[image] = file
        return files

    def merge_images(self, images: list, per: int = 3) -> Image:
        final = Image.new("RGB", size=self.image_default_size)
        x = 0
        y = 0
        pixels = self.image_default // per
        for image in images:
            image = image.resize((pixels, pixels))
            final.paste(image, (x, y))
            if x == self.image_default or x + pixels == self.image_default:
                x = 0
            else:
                x += pixels
                continue
            if y == self.image_default or y + pixels == self.image_default:
                y = 0
            else:
                y += pixels
        return final

    @staticmethod
    def get_server_lastfm(ctx):
        users = []
        for member in ctx.guild.members:
            if lastfm := ctx.bot.data.users.get(member.id).lastfm:
                users.append((member, lastfm))
        return users

    @staticmethod
    def get_intial_y(height):
        center_of_middle = 150 / 2
        y = center_of_middle - (height / 2)
        return height, y

    @staticmethod
    def get_x(font, string):
        center_of_right = 145 + (250 / 2)
        width, height = font.getsize(string)
        x = center_of_right - (width / 2)
        return x

    @staticmethod
    def get_playcount_x(font, string):
        width, height = font.getsize(string)
        x = 400 - 15 - width
        return x


def setup(bot):
    bot.add_cog(LastFM(bot))
    print("COGS > Reloaded cogs.lastfm")

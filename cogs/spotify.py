from core.exceptions import NotSpotifyPremium, NoSpotifyAccount, NoSpotifyDevice
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import discord
import aiohttp
import asyncio
import textwrap


class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CLIENT_ID = bot.config.keys.spotify.id
        self.CLIENT_SECRET = bot.config.keys.spotify.secret
        self.ACCOUNTS = "https://accounts.spotify.com"
        self.API = "https://api.spotify.com"
        self.REDIRECT_URI = "https://myer.wtf/spotify"
        self.AUTHENTICATION_URL = f"https://accounts.spotify.com/authorize?client_id={self.CLIENT_ID}&response_type" \
                                  f"=code&scope=streaming%20user-read-playback-state&redirect_uri=https://myer.wtf" \
                                  f"/spotify "
        self.sessions = {}
        self.template = Image.open("static/nowplaying.png")
        self.font = ImageFont.truetype("static/calibri.ttf", 20)

    @commands.group(invoke_without_subcommand=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def spotify(self, ctx):
        return

    @spotify.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def set(self, ctx):
        await ctx.reply(embed=ctx.bot.static.embed(ctx, "Sent you a DM with an authentication link"))
        await ctx.author.send(f"<{self.AUTHENTICATION_URL}>", embed=ctx.bot.static.embed(ctx, "Log in to your Spotify "
                                                                                              "account using this "
                                                                                              "link.\n "
                                                                                              "If successful, the page "
                                                                                              "will display a code.\n"
                                                                                              "Copy and paste the "
                                                                                              "code into "
                                                                                              "this DM channel."))
        code = await ctx.bot.wait_for("message",
                                      check=lambda m: m.author == ctx.author and m.channel == ctx.author.dm_channel)
        token = await self.get_token(code.content)
        if token:
            ctx.bot.data.users.set(ctx.author.id, "spotify", token)
            return await code.reply(embed=ctx.bot.static.embed(ctx, "Successfully logged in to your Spotify account"))

    @spotify.command(aliases=["unverify", "unlink"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def unset(self, ctx):
        reset = ctx.bot.data.users.delete(ctx.author.id, "spotify")
        return await ctx.reply(
            embed=ctx.bot.static.embed(ctx, f"Logged out of your Spotify account" if reset else "You were not logged "
                                                                                                "into Spotify!"))

    @spotify.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def listenalong(self, ctx, member: discord.Member):
        spotify = ctx.bot.data.users.get(ctx.author.id).spotify
        if spotify.refresh:
            songs = 1
            track, activity, position, _ = self.get_member_now_playing(member)
            if not track:
                return await ctx.reply(embed=ctx.bot.static.embed(ctx, f"{member.mention} is not listening to "
                                                                       f"anything on Spotify!"))
            await self.set_song(spotify, track, position, ctx.author.id)
            await ctx.reply(f"`#{songs}`",
                            file=discord.File(ctx.bot.static.image_to_bytes(await self.get_image(activity)),
                                              filename="song.png"))
            retries = 0
            async for song, activity, position in self.continue_getting_songs(member):
                now_playing = await self.get_now_playing(spotify, ctx.author.id)
                if not song or not position:
                    if retries < 15:
                        retries += 1
                        await asyncio.sleep(3)
                        continue
                    else:
                        return await ctx.reply(embed=ctx.bot.static.embed(ctx, f"{member.mention} stopped listening "
                                                                               f"to music!"))
                elif not now_playing:
                    return await ctx.reply(embed=ctx.bot.static.embed(ctx, "Spotify session was interrupted"))
                elif (not now_playing.get("is_playing") or now_playing.get("item", {}).get("uri") != song) and song == track:
                    return await ctx.reply(embed=ctx.bot.static.embed(ctx,
                                                                      f"Playback was unsynced with {member.mention}'s. "
                                                                      f" If you meant to stop listening along, "
                                                                      f"ignore this message. Otherwise, "
                                                                      f"try again"))
                elif song != track:
                    songs += 1
                    await ctx.reply(f"`#{songs}`",
                                    file=discord.File(ctx.bot.static.image_to_bytes(await self.get_image(activity)),
                                                      filename="song.png"))
                    await self.set_song(spotify, song, position, ctx.author.id)
                    track = song
        else:
            raise NoSpotifyAccount

    def get_member_now_playing(self, member):
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                position = activity.duration.seconds - (activity.end - self.bot.static.time()).seconds
                time_to_end = activity.duration.seconds - position
                return f"spotify:track:{activity.track_id}", \
                       activity, \
                       activity.duration.seconds - (activity.end - self.bot.static.time()).seconds, \
                       time_to_end
        return None, None, None, None

    async def continue_getting_songs(self, member):
        while True:
            await asyncio.sleep(3)  # check every two seconds
            track, activity, position, _ = self.get_member_now_playing(member)
            yield track, activity, position

    async def get_token(self, code) -> dict:
        async with aiohttp.request("POST", f"{self.ACCOUNTS}/api/token", data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.REDIRECT_URI,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET
        }) as response:
            if response.status == 200:
                response = await response.json()
                return response

    async def refresh_token(self, code, user) -> dict:
        async with aiohttp.request("POST", f"{self.ACCOUNTS}/api/token", data={
            "grant_type": "refresh_token",
            "refresh_token": code,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET
        }) as response:
            if response.status == 200:
                response = await response.json()
                response.update({"refresh_token": response.get("refresh_token", code)})
                self.bot.data.users.set(user, "spotify", response)
                return response

    async def set_song(self, spotify, song, position, user):
        async with aiohttp.request("PUT",
                                   f"{self.API}/v1/me/player/play",
                                   json={
                                       "uris": [song],
                                       "position_ms": position * 1000
                                   },
                                   headers={
                                       "Authorization": f"Bearer {spotify.token}"
                                   }) as response:
            if response.status == 401:
                await self.refresh_token(spotify.refresh, user)
                spotify = self.bot.data.users.get(user).spotify
                return await self.set_song(spotify, song, position, user)
            elif response.status == 403:
                raise NotSpotifyPremium
            elif response.status == 404:
                raise NoSpotifyDevice
            elif response.status != 204:
                response = await response.json()
                return response

    async def get_now_playing(self, spotify, user):
        async with aiohttp.request("GET",
                                   f"{self.API}/v1/me/player/?market=from_token",
                                   headers={
                                       "Authorization": f"Bearer {spotify.token}"
                                   }) as response:
            if response.status == 401:
                await self.refresh_token(spotify.refresh, user)
                spotify = self.bot.data.users.get(user).spotify
                return await self.get_now_playing(spotify, user)
            elif response.status == 204:
                return None
            elif response.status == 200:
                return await response.json()

    async def get_image(self, activity):
        cover = self.bot.static.image_to_pil(await self.bot.static.get_image(activity.album_cover_url))
        cover = cover.resize((129, 129))
        image = self.template.copy()
        draw = ImageDraw.Draw(image)
        image.paste(cover, (11, 11))
        string = f"{activity.artist} ― {activity.title}"
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
        return image

    # these are all magic number functions
    # stole these from lastfm.py Xd
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


def setup(bot):
    bot.add_cog(Spotify(bot))
    print("COGS > Reloaded cogs.spotify")

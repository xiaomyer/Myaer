from discord.ext import commands
import discord
import aiohttp


class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CLIENT_ID = bot.config.keys.spotify.id
        self.CLIENT_SECRET = bot.config.keys.spotify.secret
        self.ACCOUNTS = "https://accounts.spotify.com"
        self.API = "https://api.spotify.com"
        self.REDIRECT_URI = "https://myer.wtf/spotify"
        self.AUTHENTICATION_URL = f"https://accounts.spotify.com/authorize?client_id={self.CLIENT_ID}&response_type" \
                                  f"=code&scope=streaming&redirect_uri=https://myer.wtf/spotify"
        self.sessions = {}

    @commands.group(invoke_without_subcommand=True)
    async def spotify(self, ctx):
        return

    @spotify.command()
    async def set(self, ctx):
        await ctx.author.send(f"<{self.AUTHENTICATION_URL}>")
        code = await ctx.bot.wait_for("message",
                                      check=lambda m: m.author == ctx.author and m.channel == ctx.author.dm_channel)
        token = await self.get_token(code.content)
        if token:
            ctx.bot.data.users.set(ctx.author.id, "spotify", token)

    @spotify.command()
    async def play(self, ctx, song):
        spotify = ctx.bot.data.users.get(ctx.author.id).spotify
        if spotify:
            await self.set_song(spotify.token, song, 0)

    @spotify.command()
    async def listenalong(self, ctx, member: discord.Member):
        spotify = ctx.bot.data.users.get(ctx.author.id).spotify
        if spotify:
            track, position = self.get_member_now_playing(member)
            if not track:
                return await ctx.reply("no")
            await self.set_song(spotify.token, track, position)

    def get_member_now_playing(self, member):
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                return f"spotify:track:{activity.track_id}", activity.duration.seconds - (activity.end - self.bot.static.time()).seconds
        return None

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

    async def set_song(self, token, song, position):
        async with aiohttp.request("PUT",
                                   f"{self.API}/v1/me/player/play",
                                   json={
                                       "uris": [song],
                                       "position_ms": position * 1000
                                   },
                                   headers={
                                       "Authorization": f"Bearer {token}"
                                   }) as response:
            if response.status != 204:
                response = await response.json()
                print(response)
                return response


def setup(bot):
    bot.add_cog(Spotify(bot))
    print("COGS > Reloaded cogs.spotify")

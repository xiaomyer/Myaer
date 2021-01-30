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

import time

import hypixelaPY
from .exceptions import NoMinecraftUUID


async def Hypixel_(bot, api: str):
    client = HypixelClient_(bot)
    await client._init_client(api)
    return client


class HypixelClient_:
    # wrapper around the hypixel api library i'm using
    # that also happens to be mine
    # basically this includes a bunch of bot specific features and caching
    def __init__(self, bot):
        self.bot = bot

    async def _init_client(self, api: str):
        self.hypixel = await hypixelaPY.Hypixel(api)
        self.player = Player(self.bot, self.hypixel)
        self.guild = Guild(self.bot, self.hypixel)
        self.leaderboards = Leaderboards(self.bot, self.hypixel)


class Player:
    def __init__(self, bot, hypixel):
        self.hypixel = hypixel
        self.bot = bot

    async def get(self, *, ctx=None, input_: str, uuid: str = "", name: str = ""):
        if not (bool(uuid) or bool(name) or bool(input_)):
            if user := self.bot.data.users.get(ctx.author.id):
                uuid = user.minecraft_uuid
            else:
                uuid = None
        else:
            if bool(input_):
                if user := await self.bot.static.try_user_convert(self.bot, ctx, input_):
                    if user.mentioned_in(ctx.message):
                        uuid = self.bot.data.users.get(user.id).minecraft_uuid
                if input_.isdigit():
                    input_ = int(input_)
                    if bool(self.bot.get_user(input_)):
                        uuid = self.bot.data.users.get(input_).minecraft_uuid
        if not uuid and not (bool(uuid) or bool(name) or bool(input_)):  # if uuid wasn't retrieved from a call with
            # no inputs, then the user was not in the database
            raise NoMinecraftUUID
        return await self.hypixel.player.get(input_=input_, uuid=uuid, name=name)


class Leaderboards:
    def __init__(self, bot, hypixel):
        self.bot = bot
        self.hypixel = hypixel
        self.cache = {}

    async def get_players(self, leaderboard):  # the leaderboard that i want the players for
        if self.cache.get(str(leaderboard)) and time.time() - self.cache.get(str(leaderboard))[1] < 3600:
            players = self.cache.get(str(leaderboard))[0]
        else:
            players = await leaderboard.get_players()
            self.cache[str(leaderboard)] = players, time.time()
        return players


class Guild:
    def __init__(self, bot, hypixel):
        self.bot = bot
        self.hypixel = hypixel

    async def get(self, *, name: str = "", uuid: str = "", input_: str = ""):
        try:
            return await self.hypixel.guild.get(name=name, uuid=uuid, input_=input_)
        except hypixelaPY.NoGuildFoundError:  # this is easier for my purposes
            return None

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

import imperatoraPY
from .exceptions import NoMinecraftUUID


async def Imperator_(bot, api: str):
    client = ImperatorClient(bot)
    await client._init_client(api)
    return client


class ImperatorClient:
    # wrapper around the imperator api library i'm using
    # that also happens to be mine
    # basically this includes a bunch of bot specific features and caching
    def __init__(self, bot):
        self.bot = bot

    async def _init_client(self, api: str):
        self.imperator = await imperatoraPY.Imperator(api)
        self.player = Player(self.bot, self.imperator)


class Player:
    def __init__(self, bot, imperator):
        self._imperator = imperator
        self.bot = bot

    async def get(self, *, ctx=None, query: str, uuid: str = "", name: str = ""):
        if not (bool(uuid) or bool(name) or bool(query)):
            if user := self.bot.data.users.get(ctx.author.id):
                uuid = user.minecraft_uuid
            else:
                uuid = None
        else:
            if bool(query):
                if user := await self.bot.static.try_user_convert(self.bot, ctx, query):
                    if user.mentioned_in(ctx.message):
                        uuid = self.bot.data.users.get(user.id).minecraft_uuid
                if query.isdigit():
                    query = int(query)
                    if bool(self.bot.get_user(query)):
                        uuid = self.bot.data.users.get(query).minecraft_uuid
        if not uuid and not (bool(uuid) or bool(name) or bool(query)):  # if uuid wasn't retrieved from a call with
            # no inputs, then the user was not in the database
            raise NoMinecraftUUID
        return await self._imperator.fetch.player(query=query, name=name, uuid=uuid)

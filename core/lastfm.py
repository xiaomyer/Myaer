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

from .exceptions import NoLastFMUsername
import lastfmpy


async def LastFM_(bot, api: str):
    client = LastFMClient_(bot)
    await client._init_client(api)
    return client


class LastFMClient_:
    def __init__(self, bot):
        self.bot = bot

    async def _init_client(self, api: str):
        self.client = await lastfmpy.LastFM(api)

    async def get_username(self, *, ctx=None, username=None):
        if not bool(username):
            if username := self.bot.data.users.get(ctx.author.id):
                username = username.lastfm
            else:
                username = None
        else:
            if bool(username):
                if user := await self.bot.static.try_user_convert(self.bot, ctx, username):
                    if user.mentioned_in(ctx.message):
                        username = self.bot.data.users.get(username.id).lastfm
                if username.isdigit():
                    user = int(username)
                    if bool(self.bot.get_user(user)):
                        username = self.bot.data.users.get(user).lastfm
        if not bool(username):
            raise NoLastFMUsername
        return username

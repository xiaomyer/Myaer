"""
MIT License

Copyright (c) 2020 myerfire

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

from discord.ext import commands
from datetime import datetime
import discord


class Static:
    def __init__(self):
        self.arrow = "➤"
        self.star = "✫"
        self.startup_time = datetime.utcnow()
        self.user_converter = commands.UserConverter()
        self.admin = discord.Permissions(8)
        self.STARTUP_TIME_FORMAT = "%A, %b %d, %Y - %m/%d/%Y - %I:%M:%S %p"
        self.CREATION_TIME_FORMAT = "%m/%d/%Y - %I:%M:%S %p"
        self.crafthead = Crafthead()

    def time(self):
        return datetime.now()

    def embed(self, ctx, description):
        # common embed template i use is color=ctx.author.color, timestamp=ctx.message.created_at, description=message
        return discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=description
        )


class Crafthead:
    def __init__(self):
        self.CRAFTHEAD = "https://crafthead.net"

    def avatar(self, input_):
        return f"{self.CRAFTHEAD}/helm/{input_}.png"
        # helm returns regular avatar + helm and only avatar if the player no helm

    def skin(self, input_):
        return f"{self.CRAFTHEAD}/skin/{input_}.png"

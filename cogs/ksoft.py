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
from discord.ext import commands, menus


class KSoft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logo = "https://cdn.ksoft.si/images/Logo1024-W.png"

    @commands.command(aliases=["lyric"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def lyrics(self, ctx: commands.Context, *query):
        if not query or query[0] == "np":
            username = await ctx.bot.lastfm.get_username(ctx=ctx)
            song = await ctx.bot.lastfm.client.user.get_now_playing(username)
            if not song:
                return await ctx.reply(embed=ctx.bot.static.embed(ctx, description="Not currently playing anything"))
            query = f"{song.artist.name} - {song.name}"
        else:
            query = " ".join(list(query))
        data = await ctx.bot.ksoft.music.lyrics(query)
        song = data[0]
        lyrics_split = song.lyrics.split("\n")
        lyrics_paginator = menus.MenuPages(
            source=ctx.bot.static.paginators.codeblock(lyrics_split, ctx, discord.Embed(
                title=song.name,
                color=ctx.author.color,
                timestamp=ctx.message.created_at,
            ).set_thumbnail(
                url=song.album_art
            ).set_author(
                name=song.artist
            ).set_footer(
                text="Powered by KSoft.SI",
                icon_url=self.logo
            )),
            clear_reactions_after=True
        )
        await lyrics_paginator.start(ctx)


def setup(bot):
    bot.add_cog(KSoft(bot))
    print("COGS > Reloaded cogs.ksoft")

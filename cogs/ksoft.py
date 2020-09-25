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

from core.paginators import Lyrics
from ratelimit import limits

import discord
import ksoftapi
from discord.ext import commands, menus


class KSoft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logo = "https://cdn.ksoft.si/images/Logo1024-W.png"

    @commands.command(name="lyrics", aliases=["lyric"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def lyrics(self, ctx: commands.Context, *, query: str):
        data = await ctx.bot.ksoft.music.lyrics(query)
        song = data[0]
        lyrics_split = song.lyrics.split("\n")
        lyrics_paginator = menus.MenuPages(
            source=Lyrics(lyrics_split, ctx, song, footer_url=self.logo),
            clear_reactions_after=True
        )
        await lyrics_paginator.start(ctx)

#     @commands.group(name="images", aliases=["image"], invoke_without_command=True)
#     @commands.max_concurrency(1, per=commands.BucketType.user)
#     async def images(self, ctx: commands.Context):
#         await ctx.send(embed=discord.Embed(
#             title="Image Commands",
#             color=ctx.author.color,
#             timestamp=ctx.message.created_at,
#             description="""```
# /image random <tag> (/image tags for tag list)
# /image meme
# /image cute
# /image wikihow
# /image reddit <subreddit>
# /image tags
# ```"""
#         ))
#
#     @images.command(name="random")
#     @commands.max_concurrency(1, per=commands.BucketType.user)
#     async def images_random(self, ctx, *, tag: str):
#         try:
#             image = await get_random_image(ctx, tag)
#             await ctx.send(embed=discord.Embed(
#                 color=ctx.author.color,
#                 timestamp=ctx.message.created_at,
#                 title=tag,
#             ).set_image(
#                 url=image.url
#             ).set_footer(
#                 text="Powered by KSoft.SI",
#                 icon_url=self.logo
#             ))
#         except ksoftapi.errors.APIError:
#             return await ctx.send(embed=discord.Embed(
#                 color=ctx.author.color,
#                 timestamp=ctx.message.created_at,
#                 description="Invalid image tag"
#             ))


@limits(calls=4, period=1)
async def get_random_image(ctx, tag: str, nsfw: bool = False):
    return await ctx.bot.ksoft.images.random_image(tag, nsfw=nsfw)


def setup(bot):
    bot.add_cog(KSoft(bot))
    print("Reloaded cogs.ksoft")

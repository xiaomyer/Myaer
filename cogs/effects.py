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

import aiohttp
import discord
import io
from discord.ext import commands, menus
from PIL import Image, ImageFilter


class Effects(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_files = [".jpg", ".png", ".gif"]

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def contour(self, ctx, input_=None):
        image = await self.parse_image_url(ctx, input_)
        image = ctx.bot.static.image_to_pil(await ctx.bot.static.get_image(image))
        image = image.convert("RGB")
        image = image.filter(ImageFilter.CONTOUR)
        await ctx.send(file=discord.File(ctx.bot.static.image_to_bytes(image), filename="contour.png"))

    # @commands.command()
    # @commands.max_concurrency(1, per=commands.BucketType.user)
    # async def deepfry(self, ctx, input_=None):
    #     image = await self.parse_image_url(ctx, input_)
    #     image = ctx.bot.static.image_to_pil(await ctx.bot.static.get_image(image))
    #     image = image.convert("RGB")
    #     image = await deeppyer.deepfry(image)
    #     await ctx.send(file=discord.File(ctx.bot.static.image_to_bytes(image), filename="deepfry.png"))

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def emboss(self, ctx, input_=None):
        image = await self.parse_image_url(ctx, input_)
        image = ctx.bot.static.image_to_pil(await ctx.bot.static.get_image(image))
        image = image.convert("RGB")
        image = image.filter(ImageFilter.EMBOSS)
        await ctx.send(file=discord.File(ctx.bot.static.image_to_bytes(image), filename="emboss.png"))

    async def parse_image_url(self, ctx, input_):
        image = None
        if not input_:
            if ctx.message.attachments:
                if self.image_files in ctx.message.attachments[0].filename:
                    image = ctx.message.attachments[0].url
            else:
                image = str(ctx.author.avatar_url_as(static_format="png", size=2048))
        else:
            if user := await self.bot.static.try_user_convert(self.bot, ctx, input_):
                if user.mentioned_in(ctx.message):
                    image = str(user.avatar_url_as(static_format="png", size=2048))
            if input_.isdigit():
                input_ = int(input_)
                if user := ctx.bot.get_user(input_):
                    image = str(user.avatar_url_as(static_format="png", size=2048))
        return image


def setup(bot):
    bot.add_cog(Effects(bot))
    print("COGS > Reloaded cogs.effects")

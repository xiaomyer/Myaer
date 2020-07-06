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
from discord.ext import commands
from mathparse import mathparse


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="math", aliases=["solve", "calc"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def math(self, ctx, *, equation: str):
        try:
            parsed = mathparse.parse(equation)
        except mathparse.PostfixTokenEvaluationException:
            failed_embed = discord.Embed(
                color=ctx.author.color,
                timestamp=ctx.message.created_at,
                description=f"Parsing the expression \"{equation}\" failed. Try adding spaces between all operators and numbers"
            )
            return await ctx.send(embed=failed_embed)
        answer = discord.Embed(
            title=equation,
            description=parsed,
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        ).set_author(
            name="Math",
            icon_url=str(ctx.author.avatar_url_as(static_format="png", size=2048))
        )
        return await ctx.send(embed=answer)


def setup(bot):
    bot.add_cog(Math(bot))
    print("Reloaded commands.math")

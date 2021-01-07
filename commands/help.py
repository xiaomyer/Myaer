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

import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def help(self, ctx):
        await ctx.send(embed=discord.Embed(
            name="Help",
            description=f"""Here is some information about me
[Commands](https://github.com/MyerFire/Myaer#commands)
[GitHub](https://github.com/MyerFire/Myaer)
[Support/Info (My Discord Server)](https://inv.wtf/myerfire)
[Vote](https://discord.boats/bot/700133917264445480)
[Invite Me]({discord.utils.oauth_url(ctx.me.id, permissions=ctx.bot.static.admin)})""",
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        ).set_author(
            name="Help",
            icon_url=str(ctx.me.avatar_url_as(static_format="png", size=2048))
        ).set_footer(
            text="Made by Myer"
        ))


def setup(bot):
    bot.remove_command("help")
    print("Unloaded default help command")
    bot.add_cog(Help(bot))
    print("Reloaded commands.help")

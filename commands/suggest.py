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

from discord.ext import commands
import discord
import humanfriendly
import core.minecraft.request
import core.minecraft.verification.verification


class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="suggest", aliases=["suggestion"])
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def suggest(self, ctx, *, suggestion):
        suggestions_channel_object = ctx.bot.get_channel(self.bot.suggestions_channel)
        suggestion_embed = discord.Embed(
            name="Suggestion",
            title=f"**Suggestion from {discord.utils.escape_markdown(f'{ctx.author}')}**",
            description=f"{suggestion}",
            timestamp=ctx.message.created_at
        )
        suggestion_embed.set_footer(
            text=f"Suggested from {ctx.guild}"
        )
        await suggestions_channel_object.send(embed=suggestion_embed)
        sent_embed = discord.Embed(
            description=
            f"""Sent suggestion \"{suggestion}\" in Myer's Discord server
[Join the server](https://inv.wtf/myerfire) to see it!"""
        )
        sent_embed.set_footer(
            text="Abuse of this command will not be tolerated"
        )
        await ctx.send(embed=sent_embed)


def setup(bot):
    bot.add_cog(Suggest(bot))
    print("Reloaded commands.suggest")

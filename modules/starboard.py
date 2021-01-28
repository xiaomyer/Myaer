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

from discord.ext import commands
import discord

import datetime


class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_files = [".jpg", ".png", ".gif"]
        self.star = "⭐"
        self.starboarded = {}

    def stars_count(self, reaction):
        count = 0
        for reaction_ in reaction.message.reactions:
            if reaction.emoji == self.star:
                count = reaction_.count
        return count

    def image_parser(self, message):
        for file_type in self.image_files:
            for word in message.content.split(" "):
                if file_type in word:
                    return word
            for attachment in message.attachments:
                if file_type in attachment.filename:
                    return attachment.url

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji != self.star or not reaction.message.guild: return
        starboard = self.bot.data.guilds.get(reaction.message.guild.id).starboard
        if not starboard: return
        starboard = self.bot.get_channel(starboard)
        if message := self.starboarded.get(reaction.message.id):
            return await message.edit(content=f"{self.stars_count(reaction)} {self.star}")
        else:
            image = self.image_parser(reaction.message)
            embed = discord.Embed(
                color=reaction.message.author.color,
                timestamp=datetime.datetime.now(),
                description=f"""[Jump to Message]({reaction.message.jump_url})
            {reaction.message.content}"""
            ).set_author(
                name=f"{reaction.message.author}",
                icon_url=f"{reaction.message.author.avatar_url_as(static_format='png', size=2048)}"
            )
            if image:
                embed.set_image(
                    url=image
                )
            message = await starboard.send(f"{self.stars_count(reaction)} {self.star}", embed=embed)
            self.starboarded[reaction.message.id] = message

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji != self.star or not reaction.message.guild: return
        starboard = self.bot.data.guilds.get(reaction.message.guild.id).starboard
        if not starboard: return
        if message := self.starboarded.get(reaction.message.id):
            if self.stars_count(reaction) == 0:
                self.starboarded.pop(reaction.message.id)
                return await message.delete()
            else:
                return await message.edit(content=f"{self.stars_count(reaction)} {self.star}")


def setup(bot):
    bot.add_cog(Starboard(bot))
    print("Reloaded modules.starboard")

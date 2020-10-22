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


import datetime
import discord
from discord.ext import commands

import core.config.guilds
import core.static.static


class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.star = "⭐"

    async def amount_of_stars(self, reaction):
        return [reaction_.count for reaction_ in reaction.message.reactions if reaction_.emoji == self.star][0]

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji != self.star or not reaction.message.guild: return
        config = await core.config.guilds.get_config(reaction.message.guild.id)
        starboard = config.get("starboard")
        starboarded = config.get("starboarded", {})
        if not starboard: return
        starboard_channel = self.bot.get_channel(starboard)
        if starboarded.get(str(reaction.message.id)): # i really don't understand why tinydb refuses to save the key
            # as an int
            starboard_message = starboarded.get(str(reaction.message.id)) # i really don't understand why tinydb
            # refuses to save the key as an int
            return await (await starboard_channel.fetch_message(starboard_message)).edit(content=f"{await self.amount_of_stars(reaction)} {self.star}")
        message = await starboard_channel.send(f"{await self.amount_of_stars(reaction)} {self.star}", embed=discord.Embed(
            color=user.color,
            timestamp=datetime.datetime.now(),
            description=reaction.message.content
        ).set_author(
            name=f"{reaction.message.author} (click to jump to message)",
            icon_url=reaction.message.author.avatar_url_as(static_format="png", size=2048),
            url=reaction.message.jump_url
        ))
        starboarded[reaction.message.id] = message.id
        await core.config.guilds.set_key(reaction.message.guild.id, "starboarded", starboarded)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji != self.star or not reaction.message.guild: return
        config = await core.config.guilds.get_config(reaction.message.guild.id)
        starboard = config.get("starboard")
        starboarded = config.get("starboarded", {})
        if not starboard: return
        starboard_channel = self.bot.get_channel(starboard)
        if not starboarded: return
        starboard_message = starboarded.get(str(reaction.message.id))   # i really don't understand why tinydb
        # refuses to save the key as an int
        if not starboard_message: return
        starboard_message = await starboard_channel.fetch_message(starboard_message)
        if self.star not in [reaction_.emoji for reaction_ in reaction.message.reactions]:
            return await starboard_message.delete()
        else:
            return await starboard_message.edit(content=f"{await self.amount_of_stars(reaction)} {self.star}")


def setup(bot):
    bot.add_cog(Starboard(bot))
    print("Reloaded modules.starboard")
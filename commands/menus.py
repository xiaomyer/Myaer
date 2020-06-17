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

from discord.ext import commands, menus
import discord

class Menu(menus.ListPageSource):
	def __init__(self, data):
		super().__init__(data, per_page=10)

	async def format_page(self, menu, entries):
		offset = menu.current_page * self.per_page
		page_embed = discord.Embed(
			name = "Page",
			description = '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))
		)
		return page_embed

class MenusTest(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name = "menutest")
	async def menustest(self, ctx):
		pages = menus.MenuPages(source=Menu(range(1, 100)), clear_reactions_after=True)
		await pages.start(ctx)

def setup(bot):
	bot.add_cog(MenusTest(bot))
	print("Reloaded cogs.menus_test")

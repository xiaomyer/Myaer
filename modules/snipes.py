"""
MIT License

Copyright (c) 2020 GamingGeek, MyerFire

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

# yoinked from fire's codebase because snipes were removed from fire and i want snipes
# implementation somewhat changed 
# https://raw.githubusercontent.com/FireDiscordBot/bot/e66f0367ce87ec00f23a0f24afd0afe4592c5037/modules/snipes.py

from discord.ext import commands
import discord
import typing
import re

class Snipes(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.snipes = {}
		self.edit_snipes = {}

	async def snipe_embed(self, context_channel, message, user, edited = False):
		if not message.system_content and message.embeds and message.author.bot:
			return message.embeds[0]
		msg = None
		lines = []
		color = message.author.color
		embed = discord.Embed(
			color = color,
			timestamp = message.created_at
		)
		if message.system_content:
			urlre = r"((?:https:\/\/|http:\/\/)[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*(?:\.png|\.jpg|\.jpeg|\.gif|\.gifv|\.webp)))"
			search = re.search(urlre, message.system_content)
			if search and not message.attachments:
				msg = message.system_content.replace(search.group(0), "").split("\n")
				embed.set_image(url = search.group(0))
			if not msg:
				msg = message.system_content.split("\n")
			for line in msg:
				lines.append(f"{line}")
			if lines:
				embed.description = "\n".join(lines)
		embed.set_author(name = str(message.author), icon_url = str(message.author.avatar_url_as(static_format="png", size = 2048)))
		if message.attachments and not edited:
			embed.add_field(name="Attachment(s)", value="\n".join([attachment.filename for attachment in message.attachments]) + "\n\n__Attachment URLs are invalidated once the message is deleted.__")
		if message.channel != context_channel:
			embed.set_footer(text = f"Sniped by: {user} | in channel: #{message.channel.name}")
		else:
			embed.set_footer(text = f"Sniped by: {user}")
		return embed

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		try:
			del self.snipes[guild.id]
		except KeyError:
			pass

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		try:
			del self.snipes[channel.guild.id][channel.id]
		except KeyError:
			pass

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if not message.guild:
			return
		try:
			self.snipes[message.guild.id][message.author.id] = message
		except KeyError:
			self.snipes[message.guild.id] = {message.author.id: message}
		if message.guild and not message.author.bot:
			try:
				self.snipes[message.guild.id][message.channel.id] = message
			except KeyError:
				self.snipes[message.guild.id] = {message.channel.id: message}

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if not before.guild:
			return
		try:
			self.edit_snipes[before.guild.id][before.author.id] = before
		except KeyError:
			self.edit_snipes[before.guild.id] = {before.author.id: before}
		if before.guild and not before.author.bot:
			try:
				self.edit_snipes[before.guild.id][before.channel.id] = before
			except KeyError:
				self.edit_snipes[before.guild.id] = {before.channel.id: before}

	@commands.command(name = "snipe")
	async def snipe(self, ctx, *, target: typing.Union[discord.Member, discord.TextChannel] = None):
		if not target:
			target = ctx.channel

		snipetype = self.snipes

		guild_snipes = snipetype.get(ctx.guild.id, None)
		if not guild_snipes:
			nothing_to_snipe_member_embed = discord.Embed(
				description = f"Nothing to snipe for <@{target.id}>" if isinstance(target, discord.Member) else f"Nothing to snipe for <#{target.id}>"
			)
			await ctx.send(embed = nothing_to_snipe_member_embed)
			return
		message = guild_snipes.pop(target.id, None)  # A message can now only be sniped once
		if not message:
			nothing_to_snipe_member_embed = discord.Embed(
				description = f"Nothing to snipe for <@{target.id}>" if isinstance(target, discord.Member) else f"Nothing to snipe for <#{target.id}>"
			)
			await ctx.send(embed = nothing_to_snipe_member_embed)
			return

		if message.channel.is_nsfw() and not ctx.channel.is_nsfw():
			cannot_snipe_nsfw_embed = discord.Embed(
				description = "Cannot snipe a message from an NSFW channel in a non-NSFW channel"
			)
			await ctx.send(embed = cannot_snipe_nsfw_embed)
			return

		if not message.content and message.embeds and message.author.bot:
			await ctx.send(
				content = f"Raw embed from {message.author} in {message.channel.mention}",
				embed = await self.snipe_embed(ctx.channel, message, ctx.author, edited = bool(message.edited_at))
			)
		else:
			await ctx.send(embed = await self.snipe_embed(ctx.channel, message, ctx.author, edited = bool(message.edited_at)))

	@commands.command(name = "esnipe")
	async def edit_snipe(self, ctx, *, target: typing.Union[discord.Member, discord.TextChannel] = None):
		if not target:
			target = ctx.channel

		snipetype = self.edit_snipes

		guild_snipes = snipetype.get(ctx.guild.id, None)
		if not guild_snipes:
			nothing_to_snipe_member_embed = discord.Embed(
				description = f"Nothing to snipe for <@{target.id}>" if isinstance(target, discord.Member) else f"Nothing to snipe for <#{target.id}>"
			)
			await ctx.send(embed = nothing_to_snipe_member_embed)
			return
		message = guild_snipes.pop(target.id, None)  # A message can now only be sniped once
		if not message:
			nothing_to_snipe_member_embed = discord.Embed(
				description = f"Nothing to snipe for <@{target.id}>" if isinstance(target, discord.Member) else f"Nothing to snipe for <#{target.id}>"
			)
			await ctx.send(embed = nothing_to_snipe_member_embed)
			return

		if message.channel.is_nsfw() and not ctx.channel.is_nsfw():
			cannot_snipe_nsfw_embed = discord.Embed(
				description = "Cannot snipe a message from an NSFW channel in a non-NSFW channel"
			)
			await ctx.send(embed = cannot_snipe_nsfw_embed)
			return

		if not message.content and message.embeds and message.author.bot:
			await ctx.send(
				content = f"Raw embed from {message.author} in {message.channel.mention}",
				embed = await self.snipe_embed(ctx.channel, message, ctx.author, edited = bool(message.edited_at))
			)
		else:
			await ctx.send(embed = await self.snipe_embed(ctx.channel, message, ctx.author, edited = bool(message.edited_at)))

def setup(bot):
	bot.add_cog(Snipes(bot))
	print("Reloaded modules.snipes")

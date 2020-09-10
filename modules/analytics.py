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

from core.paginators import Analytics_, SessionAnalytics

from discord.ext import commands, menus, tasks

import json

with open("analytics.json", mode="r+") as stats_json:
    overall_stats = json.load(stats_json)


async def save_overall_stats():
    with open("analytics.json", mode="w") as stats:
        json.dump(overall_stats, stats, indent=2)


class Analytics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = {}
        # self.save_overall_stats.start()

    # def cog_unload(self):
        # self.save_overall_stats.cancel()

    # @tasks.loop(seconds=1)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if self.session.get(ctx.command.qualified_name):
            self.session[ctx.command.qualified_name] += 1
        else:
            self.session[ctx.command.qualified_name] = 1
        if overall_stats.get(ctx.command.qualified_name):
            overall_stats[ctx.command.qualified_name] += 1
        else:
            overall_stats[ctx.command.qualified_name] = 1
        await save_overall_stats()

    @commands.group(name="analytics", invoke_without_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def analytics(self, ctx):
        analytics_paginator = menus.MenuPages(
            source=Analytics_(format_analytics(overall_stats), ctx, total_commands(overall_stats)),
            clear_reactions_after=True
        )
        await analytics_paginator.start(ctx)

    @analytics.command(name="session")
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def session_analytics(self, ctx):
        analytics_paginator = menus.MenuPages(
            source=SessionAnalytics(format_analytics(self.session), ctx, total_commands(self.session)),
            clear_reactions_after=True
        )
        await analytics_paginator.start(ctx)


def format_analytics(data):
    return [f"{key}: {value}" for key, value in sorted(data.items(), key=lambda k, v: v, reverse=True)]


def total_commands(data):
    total = 0
    for key in data:
        total += data[key]
    return total


def setup(bot):
    bot.add_cog(Analytics(bot))
    print("Reloaded modules.analytics")

import logging
import time

import arrow
import discord
from discord.ext import commands


import config
from .utils import checks

log = logging.getLogger(__name__)


class General:
    """General"""

    def __init__(self, bot):
        self.bot = bot
        self.voice_connection = None

    @commands.command(name='uptime')
    async def uptime(self, ctx):
        """Bot Uptime."""
        total_seconds = float(time.time() - config.BOTUPTIME)
        # Helper vars:
        MINUTE = 60
        HOUR = MINUTE * 60
        DAY = HOUR * 24

        # Get the days, hours, etc:
        days = int(total_seconds / DAY)
        hours = int((total_seconds % DAY) / HOUR)
        minutes = int((total_seconds % HOUR) / MINUTE)
        seconds = int(total_seconds % MINUTE)

        # Build up the pretty string
        # (like this: "N days, N hours, N minutes, N seconds")
        string = ""
        if days > 0:
            string += str(days) + " " + (days == 1 and "day" or "days") + ", "
        if len(string) > 0 or hours > 0:
            string += str(hours) + " " + (hours == 1 and "hour" or "hours") + ", "
        if len(string) > 0 or minutes > 0:
            string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes") + ", "
        string += str(seconds) + " " + (seconds == 1 and "second" or "seconds")

        await ctx.send(string)

    @commands.command(name='clear')
    @checks.is_admin()
    async def clear(self, ctx, lines: int = 1):
        """
        Clears a number of lines from chat
        Permissions: Needs admin permissions
        """
        dellist = await ctx.channel.history(limit=int(lines) + 1).flatten()
        await ctx.channel.delete_messages(dellist)

    @commands.command(name='server')
    async def server(self, ctx):
        """
        Displays server info
        Usage: !server
        """
        server = ctx.guild
        embed = discord.Embed(title=server.name, description="", color=ctx.me.color)
        embed.set_thumbnail(url=server.icon_url)

        serverinfo = f"Owner: {server.owner}\n" \
                     f"Created: {arrow.get(server.created_at).humanize()}\n" \
                     f"Members: {server.member_count}\n" \
                     f"Region: {server.region}\n" \
                     f"Features: {', '.join(server.features)}"
        embed.add_field(name="Server Information", value=serverinfo)

        member_list = list(server.members)
        status_list = [member.status.value for member in member_list]

        membersinfo = (f"Online: {status_list.count('online')}\n"
                       f"Idle: {status_list.count('idle')}\n"
                       f"Dnd: {status_list.count('dnd')}\n"
                       f"Offline: {status_list.count('offline')}")

        embed.add_field(name="Channels", value=f"{len(server.channels)}", inline=True)
        embed.add_field(name="Roles", value=f"{len(server.roles)}", inline=True)
        embed.add_field(name="Members", value=membersinfo, inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
    log.info("Cog loaded: General")

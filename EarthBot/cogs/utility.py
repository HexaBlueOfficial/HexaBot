import discord
from datetime import datetime
from discord.ext import commands

class Utility(commands.Cog):
    """The cog for Earth's utilities."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.launch_time = datetime.utcnow()
    
    @commands.command(name="uptime", aliases=["up", "upt"])
    async def uptime(self, ctx):
        """Shows an Embed with Earth's uptime."""

        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        e = discord.Embed(title="Uptime", color=0x00a8ff, description=f"The bot has been online for:\n{days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Last Restart", value="The bot was last restarted on {} UTC".format(self.bot.launch_time.strftime("%A, %d %B %Y at %H:%M")), inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @commands.command(name="ping", aliases=["latency", "lat"])
    async def ping(self, ctx):
        """Shows an Embed with Earth's ping latency."""

        ping = self.bot.latency * 1000
        pingr = round(ping, 1)
        e = discord.Embed(title="Ping Latency", color=0x00a8ff, description=f"My ping latency is {pingr}ms. It's the time it takes for my host's servers to reach Discord.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Utility(bot))
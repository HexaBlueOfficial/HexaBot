import discord
import random
import asyncio
from discord.ext import commands, tasks

class Core(commands.Cog):
    """The cog for Earth's core commands."""

    def __init__(self, bot):
        self.bot = bot
        self.presence.start() # pylint: disable=no-member
    
    @tasks.loop(seconds=60.0)
    async def presence(self):
        presences = {"playing": ["with Earthlings", "around", "happily", "on Earth", "Save the Planet [Hard Mode]", "with e.help"], "watching": ["plastic in the ocean", "the globe warming", "the animals extinguish", "you help make the future better", "https://earthdiscord.gq"]}
        playorwatch = random.randint(1, 2)
        if playorwatch == 1:
            presencetouse = random.randint(0, 5)
            await self.bot.change_presence(activity=discord.Game(name=presences["playing"][presencetouse]))
        else:
            presencetouse = random.randint(0, 4)
            await self.bot.change_presence(activity=discord.Activity(name=presences["watching"][presencetouse], type=discord.ActivityType.watching))
    
    @presence.before_loop
    async def before_presence(self):
        await self.bot.wait_until_ready()
    
    @commands.command(name="info")
    async def info(self, ctx):
        """Shows information about Earth."""

        e = discord.Embed(title="About Earth", color=0x00a8ff, description="**Earth** is a private bot for the server **Planet Earth**. It has a few fun commands to keep you entertained while it also does more serious stuff.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Developer", value="<@450678229192278036>")
        e.add_field(name="Versions", value=f"Earth: v0.0.2 (Alpha 2)\ndiscord.py: v{discord.__version__}")
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @commands.command(name="arth", hidden=True)
    async def arth(self, ctx):
        """???"""

        await ctx.send("hello there")

        def check(m):
            return m.content.lower() == "general kenobi" and m.channel == ctx.channel
        
        try:
            waitfor = await self.bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            return
        else:
            await ctx.send(f"Huzzah! A man of quality! Nice one, {waitfor.author.name}!")

def setup(bot):
    bot.add_cog(Core(bot))
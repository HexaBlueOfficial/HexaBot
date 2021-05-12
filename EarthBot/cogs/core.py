import discord
import random
import asyncio
from discord.ext import commands, tasks

class Core(commands.Cog):
    """The cog for Earth's core commands."""

    def __init__(self, bot):
        self.bot = bot
        self.presence.start()
    
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
    
    @commands.Cog.listener()
    async def on_message(self, message):
        channels = [832658521731498005, 832659080841134110, 832659031847993344, 832659442213453871, 832660792397791262, 832661047398760450, 832671013753454602]
        if message.channel.id in channels:
            if message.author.id == 833038899306692639:
                return
            else:
                await message.publish()
        if message.channel.id == channels[4]:
            role = message.guild.get_role(833421078239510528)
            await message.channel.send(f"<@&{role.id}>")
        elif message.channel.id == channels[5]:
            role = message.guild.get_role(833421049587564655)
            await message.channel.send(f"<@&{role.id}>")
        elif message.channel.id == channels[6]:
            role = message.guild.get_role(833420855282237453)
            await message.channel.send(f"<@&{role.id}>")
    
    @commands.command(name="info")
    async def info(self, ctx):
        """Shows information about Earth."""

        luckyint = random.randint(1, 100)

        e = discord.Embed(title="About Earth", color=0x00a8ff, description="**Earth** is a private bot for the server **Planet Earth**. It has a few fun commands to keep you entertained while it also does more serious stuff.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Developers", value="<@450678229192278036>: `e.info`, AutoPublish, AutoPing, `e.say`, `e.cat`, `e.dog`, `e.fox`, `e.ping`, `e.uptime`, `e.userinfo`, `e.serverinfo`, `e.nitro`.\n<@598325949808771083>: `e.help`.\nOther: `e.uwu` (Inspired by <@788483848127905844>'s old code, coded by <@450678229192278036>), `e.jishaku` (External Extension).", inline=False)
        if luckyint == 69:
            e.set_field_at(0, name="Developers", value="<@450678229192278036>: `e.info`, AutoPublish, AutoPing, `e.arth`, `e.say`, `e.cat`, `e.dog`, `e.fox`, `e.ping`, `e.uptime`, `e.userinfo`, `e.serverinfo`, `e.nitro`.\n<@598325949808771083>: `e.help`.\nOther: `e.uwu` (Inspired by <@788483848127905844>'s old code, coded by <@450678229192278036>), `e.jishaku` (External Extension).", inline=False)
        e.add_field(name="Versions", value=f"Earth: v1.1.2\ndiscord.py: v{discord.__version__}", inline=False)
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
import discord
import json
import asyncpg
import random
import asyncio
from discord.ext import commands, tasks

class Core(commands.Cog):
    """The cog for Earth's core commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./postgres.json") as postgresfile:
            postgresdict = json.load(postgresfile)
        self.postgres = postgresdict["creds"]
        self.presence.start()
    
    async def pgexecute(self, sql):
        db = await asyncpg.connect(self.postgres)
        await db.execute(f'''{sql}''')
    
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
    async def on_message(self, message: discord.Message):
        if message.channel.type == discord.ChannelType.news:
            if message.author.bot:
                return
            else:
                message.publish()
        
        q = await self.pgexecute(f"SELECT {message.guild.id} FROM ping")
        for ping in q:
            channel = message.guild.get_channel(ping.splitlines()[0])
            if message.channel == channel:
                role = ping.splitlines()[1]
                await channel.send(f"<@&{role}>")
    
    @commands.command(name="info")
    async def info(self, ctx: commands.Context):
        """Shows information about Earth."""

        luckyint = random.randint(1, 100)

        e = discord.Embed(title="About Earth", color=0x00a8ff, description="**Earth** is a private bot for the server **Planet Earth**. It has a few fun commands to keep you entertained while it also does more serious stuff.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Developers", value="<@450678229192278036>: `e.info`, AutoPublish, AutoPing, `e.say`, `e.uwu`, `e.cat`, `e.dog`, `e.fox`, `e.hug`, `e.kill`, `e.gaypercent`, `e.8ball`, `e.ping`, `e.uptime`, `e.userinfo`, `e.serverinfo`, `e.nitro` and their Slash equivalents.\n<@598325949808771083>: `e.help`.\nOther: `e.jishaku` (External Extension).", inline=False)
        if luckyint == 69:
            e.set_field_at(0, name="Developers", value="<@450678229192278036>: `e.info`, AutoPublish, AutoPing, `e.arth`, `e.say`, `e.uwu`, `e.cat`, `e.dog`, `e.fox`, `e.hug`, `e.kill`, `e.gaypercent`, `e.8ball`, `e.ping`, `e.uptime`, `e.userinfo`, `e.serverinfo`, `e.nitro` and their Slash equivalents. **`e.arth` is not available as Slash!**\n<@598325949808771083>: `e.help`.\nOther: `e.jishaku` (External Extension).", inline=False)
        e.add_field(name="Versions", value=f"Earth: v1.2.1\ndiscord.py: v{discord.__version__}", inline=False)
        e.add_field(name="Credits", value="**Hosting:** [Library of Code](https://loc.sh/discord)\n**Inspiration for `e.kill`, `e.gaypercent` and `e.8ball`:** [Dank Memer](https://dankmemer.lol) bot.\n**Inspiration for `e.uwu`:** [Reddit UwUtranslator bot](https://reddit.com/u/uwutranslator)\n**Cats:** [TheCatAPI](https://thecatapi.com)\n**Dogs:** [TheDogAPI](https://thedogapi.com)\n**Foxes:** [Random Fox](https://randomfox.ca)", inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @commands.command(name="arth", hidden=True)
    async def arth(self, ctx: commands.Context):
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
    
    @commands.command(name="invite")
    async def invite(self, ctx: commands.Context):
        """Invite Earth to your server!"""

        e = discord.Embed(title="Invite Earth!", color=0x00a8ff, description="Click the link in the **Invite** field below to add **Earth** to your server.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Invite", value="https://discord.com/api/oauth2/authorize?client_id=833038899306692639&permissions=305491009&scope=bot%20applications.commands", inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @commands.command(name="support")
    async def support(self, ctx: commands.Context):
        """Join the Planet Earth server for support with the bot."""

        await ctx.send("https://discord.gg/DsARcGwwdM")

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))
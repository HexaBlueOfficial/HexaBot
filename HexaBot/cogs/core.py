import discord
import json
import random
import typing
import platform
import asyncio
import discord_slash as interactions
from discord_slash import cog_ext
from discord.ext import commands, tasks

class Core(commands.Cog):
    """Core Commands for HexaBot!"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.presence.start()
        with open("./HexaBot/HexaBot/misc/assets/embed.json") as embedfile:
            self.embed = json.load(embedfile)
    
    @tasks.loop(seconds=400.0)
    async def presence(self):
        presences = {"playing": ["with Code", "around", "with BuildABot", "with XYZ", "with everyone", "with s!help"], "watching": ["https://hexacode.tk", "https://hexacode.ml", "you", "Flamey code"]}
        playorwatch = random.randint(1, 2)
        if playorwatch == 1:
            presencetouse = random.randint(0, 1)
            await self.bot.change_presence(activity=discord.Game(name=presences["playing"][presencetouse]))
        else:
            presencetouse = random.randint(0, 1)
            await self.bot.change_presence(activity=discord.Activity(name=presences["watching"][presencetouse], type=discord.ActivityType.watching))
    
    @presence.before_loop
    async def before_presence(self):
        await self.bot.wait_until_ready()
    
    async def info(self, ctx: typing.Union[commands.Context, interactions.SlashContext]):
        luckyint = random.randint(1, 20)

        e = discord.Embed(title="Information about HexaBot", color=int(self.embed["color"], 16), description="**HexaBot** is a Bot private to the **HexaCode** server.")
        e.set_author(name=self.embed["author"] + "Core", icon_url=self.embed["icon"])
        e.set_thumbnail(url=self.embed["icon"])
        e.add_field(name="Developers", value="<@450678229192278036>: All commands and their Slash equivalents.\n<@598325949808771083>: `s!help`.\nOther: `s!jishaku` (External Extension).", inline=False)
        e.add_field(name="Versions", value=f"HexaBot: v2.0.0\nPython: v{platform.python_version()}\ndiscord.py: v{discord.__version__}", inline=False)
        e.set_image(url=self.embed["banner"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        await ctx.send(embed=e)

        if luckyint == 8:
            await ctx.author.send("Hey!")
            await ctx.author.trigger_typing()
            await asyncio.sleep(2.0)
            await ctx.author.send("You should try running `h.exabot`!")

    @commands.command(name="info")
    async def dpyinfo(self, ctx: commands.Context):
        """Shows information about HexaBot."""

        await self.info(ctx)
    
    @cog_ext.cog_subcommand(base="info", name="bot", description="Core - Shows information about HexaBot.")
    async def slashinfobot(self, ctx: interactions.SlashContext):
        await self.info(ctx)
    
    @commands.command(name="exabot", hidden=True)
    async def hexabot(self, ctx: commands.Context):
        """???"""

        await ctx.send("hi it me")

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))
import discord
import json
import aiohttp
import random
import asyncio
import discord_slash as slash
from discord.ext import commands

class Fun(commands.Cog):
    """The cog for Earth's fun commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./Earth/EarthBot/misc/lines/hug.json") as hugs:
            self.huglines = json.load(hugs)
        with open("./Earth/EarthBot/misc/lines/kill.json") as kills:
            self.killlines = json.load(kills)
        with open("./Earth/EarthBot/misc/lines/gay.json") as gays:
            self.gaylines = json.load(gays)
        with open("./Earth/EarthBot/misc/lines/8ball.json") as eightballs:
            self.balllines = json.load(eightballs)
        with open("./Earth/EarthBot/misc/lines/skittles.json") as skittles:
            self.skittles = json.load(skittles)
        with open("./Earth/EarthBot/misc/assets/embed.json") as embeds:
            self.embed = json.load(embeds)
    
    def uwufy(self, sentence: str):
        uwu = sentence.lower()
        uwu = uwu.replace("l", "w")
        uwu = uwu.replace("r", "w")
        uwu = uwu.replace("th", "d")
        uwu = uwu.replace("ove", "uv")
        return f"{uwu}, uwu *rawr* XD!"

    @commands.command(name="say")
    async def say(self, ctx: commands.Context):
        """As a normal command could create confusion, this command is only available in Slash. Use `/say`."""

        await ctx.send("As a normal command could create confusion, this command is only available in Slash. Use `/say`.")
    
    @commands.command(name="uwu")
    async def uwu(self, ctx: commands.Context, *, sentence: str):
        """Reject English, evolve to Furry."""

        await ctx.send(self.uwufy(sentence))
    
    @commands.command(name="cat")
    async def cat(self, ctx: commands.Context):
        """Shows a random image of a cat."""

        await ctx.trigger_typing()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search/") as response:
                cat = await response.json()
                catpic = cat[0]["url"]
        
        e = discord.Embed(title="Random Cat (from TheCatAPI by Aden)", color=int(self.embed["color"], 16), description="Check out TheCatAPI [here](https://thecatapi.com)!")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_image(url=catpic)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @commands.command(name="dog")
    async def dog(self, ctx: commands.Context):
        """Shows a random image of a dog."""

        await ctx.trigger_typing()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thedogapi.com/v1/images/search/") as response:
                dog = await response.json()
                dogpic = dog[0]["url"]
        
        e = discord.Embed(title="Random Dog (from TheDogAPI by Aden)", color=int(self.embed["color"], 16), description="Check out TheDogAPI [here](https://thedogapi.com)!")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_image(url=dogpic)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @commands.command(name="fox")
    async def fox(self, ctx: commands.Context):
        """Shows a random image of a fox."""

        await ctx.trigger_typing()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomfox.ca/floof/") as response:
                fox = await response.json()
                foxpic = fox["image"]
        
        e = discord.Embed(title="Random Fox (from Random Fox by xinitrc)", color=int(self.embed["color"], 16), description="Check out Random Fox [here](https://randomfox.ca)!")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_image(url=foxpic)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)

    @commands.command(name="hug")
    async def hug(self, ctx: commands.Context, member: discord.Member, *, message=None):
        """Hugs the user you want."""

        huglineint = random.randint(0, 9)
        halfpoint = self.huglines[str(huglineint)].replace("author", ctx.author.mention)
        hugline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Hug", color=int(self.embed["color"], 16), description=f"{hugline}")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        if message is not None:
            e.add_field(name=f"{ctx.author.name} included a message! They said...", value=f"{message}", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
        await ctx.message.delete()
    
    @commands.command(name="kill")
    async def kill(self, ctx: commands.Context, member: discord.Member):
        """Kills the user you want."""

        killlineint = random.randint(0, 4)
        halfpoint = self.killlines[str(killlineint)].replace("author", ctx.author.mention)
        killline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Murder", color=int(self.embed["color"], 16), description=f"{killline}")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @commands.command(name="gaypercent", aliases=["gay", "howgay"])
    async def gaypercent(self, ctx: commands.Context, *, thing=None):
        """Wanna find out how gay something is? This command is for you."""

        gay = random.randint(0, 100)
        supergay = random.randint(1, 10)

        def makeline(jsonline):
            halfpoint = self.gaylines[jsonline].replace("thing", thing)
            gayliner = halfpoint.replace("gaypercent", f"{gay}%")
            return gayliner
        
        if thing is None:
            thing = ctx.author.mention

            if supergay == 8:
                gay = gay * 10
            
            if gay == 0:
                gayline = makeline("0")
            elif gay <= 25:
                gayline = makeline("1to25")
            elif gay <= 50:
                gayline = makeline("26to50")
            elif gay <= 75:
                gayline = makeline("51to75")
            elif gay <= 99:
                gayline = makeline("76to99")
            elif gay == 100:
                gayline = makeline("100")
            elif gay > 100:
                gayline = makeline("over100")
            
            e = discord.Embed(title="Gay Percentage", color=int(self.embed["color"], 16), description=f"{gayline}")
            e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
            await ctx.send(embed=e)
        else:
            try:
                gayid = int(thing)
            except:
                if supergay == 8:
                    gay = gay * 10
            
                if gay == 0:
                    gayline = makeline("0")
                elif gay <= 25:
                    gayline = makeline("1to25")
                elif gay <= 50:
                    gayline = makeline("26to50")
                elif gay <= 75:
                    gayline = makeline("51to75")
                elif gay <= 99:
                    gayline = makeline("76to99")
                elif gay == 100:
                    gayline = makeline("100")
                elif gay > 100:
                    gayline = makeline("over100")
            
                e = discord.Embed(title="Gay Percentage", color=int(self.embed["color"], 16), description=f"{gayline}")
                e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
                e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                await ctx.send(embed=e)
            else:
                thing = self.bot.fetch_user(gayid)

                if supergay == 8:
                    gay = gay * 10
            
                if gay == 0:
                    gayline = makeline("0")
                elif gay <= 25:
                    gayline = makeline("1to25")
                elif gay <= 50:
                    gayline = makeline("26to50")
                elif gay <= 75:
                    gayline = makeline("51to75")
                elif gay <= 99:
                   gayline = makeline("76to99")
                elif gay == 100:
                    gayline = makeline("100")
                elif gay > 100:
                    gayline = makeline("over100")
            
                e = discord.Embed(title="Gay Percentage", color=int(self.embed["color"], 16), description=f"{gayline}")
                e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
                e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                await ctx.send(embed=e)
    
    @commands.command(name="8ball", aliases=["eightball"])
    async def eightball(self, ctx: commands.Context, *, question):
        """Seek an answer from the Magic 8 Ball."""

        balllineint = random.randint(0, 4)
        ballline = self.balllines[str(balllineint)]

        e = discord.Embed(title="Magic 8 Ball", color=int(self.embed["color"], 16))
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.add_field(name="Your Question", value=f"{question}", inline=False)
        e.add_field(name="The 8 Ball's Answer", value=f"{ballline}", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @commands.command(name="poll")
    async def poll(self, ctx: commands.Context):
        """As a normal command could create confusion, this command is only available in Slash. Use `/poll`."""

        await ctx.send("As a normal command could create confusion, this command is only available in Slash. Use `/poll`.")
    
    @commands.command(name="skittles", aliases=["skittleinfo", "skittlesinfo", "skittle"])
    async def skittles(self, ctx: commands.Context):
        """Gets info about a random Skittle.\nRequested by `skittlez#8168`."""

        await ctx.trigger_typing()

        skittleint = random.randint(0, 4)
        skittle = self.skittles[str(skittleint)]
        
        e = discord.Embed(title="Information about {} Skittle".format(skittle["color"]), color=int(self.embed["color"], 16))
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_thumbnail(url=skittle["thumbnail"])
        e.add_field(name="Color", value=skittle["color"], inline=False)
        e.add_field(name="Flavor", value=skittle["flavor"], inline=False)
        e.add_field(name="Developer's Rating", value=skittle["devrate"], inline=False)
        e.add_field(name="Developer's Comment", value=skittle["devcomment"], inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @commands.command(name="calculator", aliases=["calc"])
    async def calculator(self, ctx: commands.Context):
        """As a normal command could create confusion, this command is only available in Slash. Use `/calculator`."""

        await ctx.send("As a normal command could create confusion, this command is only available in Slash. Use `/calculator`.")
    
    @commands.command(name="hack")
    async def hack(self, ctx: commands.Context, user: discord.Member):
        """Hack a member (100% real)!"""

        hacking = await ctx.send("<a:aLoading:833070225334206504> **Getting logins...**")
        await asyncio.sleep(1.0)
        await hacking.edit(content="<:Yes:833293078197829642> **Logins deciphered. Select what to hack below.**")
        
        e = discord.Embed(title=f"Hack {user.name}", color=int(self.embed["color"], 16), description=f"**Hacking {user.name} ready.**")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        hackmessage = await hacking.reply(embed=e, components=[
            slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "Hack Discord", None, custom_id="discord"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.red, "Hack YouTube", None, custom_id="youtube"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.green, "Hack Twitter", None, custom_id="twitter")
            )
        ])

        waitfor = await slash.utils.manage_components.wait_for_component(self.bot, hackmessage, ["discord", "youtube", "twitter"])
        if waitfor.author_id == ctx.author.id:
            avatar = await user.avatar_url.read()
            webhook = await ctx.channel.create_webhook(name=user.name, avatar=avatar, reason="Hack command")
            if waitfor.custom_id == "discord":
                await webhook.send("I got hacked, oh fuck.")
                await webhook.send(f"FUCK! {ctx.author} HACKED ME!")
                e.description = "**DISCORD HACKED!**"
            elif waitfor.custom_id == "youtube":
                await webhook.send("I just posted a video!\nhttps://youtu.be/Blh2FCAIIgk")
                e.description = "**YOUTUBE HACKED!**"
            elif waitfor.custom_id == "twitter":
                await webhook.send("I just tweeted!\nhttps://twitter.com/theEarthNet/status/1402642068200165383")
                e.description = "**TWITTER HACKED!**"
            await waitfor.edit_origin(embed=e)
            await webhook.delete()
            
    @commands.command(name="tictactoe", aliases=["ttt", "tic_tac_toe", "tic-tac-toe"])
    async def tictactoe(self, ctx: commands.Context):
        """As a normal command could create confusion, this command is only available in Slash. Use `/tictactoe`."""

        await ctx.send("As a normal command could create confusion, this command is only available in Slash. Use `/tictactoe`.")
            
def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
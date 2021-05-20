import discord
import json
import aiohttp
import random
from discord.ext import commands, flags
from discord.ext.commands.core import command

class Fun(commands.Cog):
    """The cog for Earth's fun commands."""

    def __init__(self, bot):
        self.bot = bot
        with open("./Earth/EarthBot/misc/hug.json") as hugs:
            self.huglines = json.load(hugs)
        with open("./Earth/EarthBot/misc/kill.json") as kills:
            self.killlines = json.load(kills)
        with open("./Earth/EarthBot/misc/gay.json") as gays:
            self.gaylines = json.load(gays)
        with open("./Earth/EarthBot/misc/8ball.json") as eightballs:
            self.balllines = json.load(eightballs)
    
    def uwufy(self, sentence: str):
        uwu = sentence.lower()
        uwu = uwu.replace("l", "w")
        uwu = uwu.replace("r", "w")
        uwu = uwu.replace("th", "d")
        return f"{uwu}, uwu *rawr* XD!"
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> {sentence}"

    @flags.add_flag("-m", default="https://discord.gg/DsARcGwwdM")
    @flags.add_flag("--uwu", action="store_true")
    @flags.add_flag("-a", action="store_true")
    @flags.add_flag("-u", type=discord.User, default=None)
    @flags.add_flag("-c", type=discord.TextChannel, default=None)
    @flags.command(name="say")
    async def say(self, ctx, **flags):
        """The bot will say what you tell him to. If you find this command too confusing, type `/` into the chat and use the Slash Command version instead.\n\nFlags:\n`-m` - Message flag. Whatever you put after this flag and before the next flag will be the message repeated by the bot. If your message has more than a word, use quotation marks.\n`--uwu` - Turns your message into the UwU language.\n`-a` - Anonymization flag. Makes your message (`-m` flag content) anonymous.\n`-u` - User flag. Makes it look like another user sent your message (`-m` flag content). Works with username, username#discriminator, @mention and ID. Users outside this server will not work.\n`-c` - Channel flag. Sends the message in the channel you specify.\n\nExample command: `e.say -m "Insert cool message here." --uwu -a`.\nOutput: `insewt coow message hewe, uwu rawr XD!` (sent by Anonymous)."""

        words = ["@everyone", "@here", "<@&832657099312857124>"]
        for word in words:
            if word in flags["m"].lower():
                await ctx.author.send("Don't even try, idiot. You think I'm so stupid not to make a check?")
        
        if flags["a"]:
            if flags["c"] is None:
                avatar = await self.bot.user.avatar_url.read()
                webhook = await ctx.channel.create_webhook(name="Anonymous", avatar=avatar, reason="Say command.")
            else:
                avatar = await self.bot.user.avatar_url.read()
                webhook = await flags["c"].create_webhook(name="Anonymous", avatar=avatar, reason="Say command.")
        elif flags["u"] is not None:
            if flags["c"] is None:
                avatar = await flags["u"].avatar_url.read()
                webhook = await ctx.channel.create_webhook(name=flags["u"].name, avatar=avatar, reason="Say command.")
            else:
                avatar = await flags["u"].avatar_url.read()
                webhook = await flags["c"].create_webhook(name=flags["u"].name, avatar=avatar, reason="Say command.")
        else:
            if flags["c"] is None:
                avatar = await ctx.author.avatar_url.read()
                webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=avatar, reason="Say command.")
            else:
                avatar = await ctx.author.avatar_url.read()
                webhook = await flags["c"].create_webhook(name=ctx.author.name, avatar=avatar, reason="Say command.")

        if not flags["uwu"]:
            await webhook.send(flags["m"])
        else:
            await webhook.send(self.uwufy(flags["m"]))
        await ctx.message.delete()
        await webhook.delete()
    
    @commands.command(name="uwu")
    async def uwu(self, ctx, *, sentence: str):
        """Reject English, evolve to Furry."""

        await ctx.send(self.uwufy(sentence))
    
    @commands.command(name="cat")
    async def cat(self, ctx):
        """Shows a random image of a cat."""

        fetching = await ctx.send(self.loading("Finding a cute cat to show you..."))

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search/") as response:
                cat = await response.json()
                catpic = cat[0]["url"]
        
        e = discord.Embed(title="Random Cat (from TheCatAPI by Aden)", color=0x00a8ff, description="Check out TheCatAPI [here](https://thecatapi.com)!")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_image(url=catpic)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await fetching.edit(content=None, embed=e)
    
    @commands.command(name="dog")
    async def dog(self, ctx):
        """Shows a random image of a dog."""

        fetching = await ctx.send(self.loading("Finding a cute dog to show you..."))

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thedogapi.com/v1/images/search/") as response:
                dog = await response.json()
                dogpic = dog[0]["url"]
        
        e = discord.Embed(title="Random Dog (from TheDogAPI by Aden)", color=0x00a8ff, description="Check out TheDogAPI [here](https://thedogapi.com)!")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_image(url=dogpic)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await fetching.edit(content=None, embed=e)
    
    @commands.command(name="fox")
    async def fox(self, ctx):
        """Shows a random image of a fox."""

        fetching = await ctx.send(self.loading("Finding a cute fox to show you..."))

        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomfox.ca/floof/") as response:
                fox = await response.json()
                foxpic = fox["image"]
        
        e = discord.Embed(title="Random Fox (from Random Fox by xinitrc)", color=0x00a8ff, description="Check out Random Fox [here](https://randomfox.ca)!")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_image(url=foxpic)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await fetching.edit(content=None, embed=e)

    @commands.command(name="hug")
    async def hug(self, ctx, member: discord.Member, *, message=None):
        """Hugs the user you want."""

        huglineint = random.randint(0, 9)
        halfpoint = self.huglines[str(huglineint)].replace("author", ctx.author.mention)
        hugline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Hug", color=0x00a8ff, description=f"{hugline}")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        if message is not None:
            e.add_field(name=f"{ctx.author.name} included a message! He said...", value=f"{message}", inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
        await ctx.message.delete()
    
    @commands.command(name="kill")
    async def kill(self, ctx, member: discord.Member):
        """Kills the user you want."""

        killlineint = random.randint(0, 4)
        halfpoint = self.killlines[str(killlineint)].replace("author", ctx.author.mention)
        killline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Murder", color=0x00a8ff, description=f"{killline}")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
        await ctx.message.delete()
    
    @commands.command(name="gaypercent", aliases=["gay", "howgay"])
    async def gaypercent(self, ctx, *, thing=None):
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
            
            e = discord.Embed(title="Gay Percentage", color=0x00a8ff, description=f"{gayline}")
            e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
            e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
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
            
                e = discord.Embed(title="Gay Percentage", color=0x00a8ff, description=f"{gayline}")
                e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
                e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
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
            
                e = discord.Embed(title="Gay Percentage", color=0x00a8ff, description=f"{gayline}")
                e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
                e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
                await ctx.send(embed=e)
    
    @commands.command(name="8ball", aliases=["eightball"])
    async def eightball(self, ctx, *, question):
        """Seek an answer from the Magic 8 Ball."""

        balllineint = random.randint(0, 4)
        ballline = self.balllines[str(balllineint)]

        e = discord.Embed(title="Magic 8 Ball", color=0x00a8ff)
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Your Question", value=f"{question}", inline=False)
        e.add_field(name="The 8 Ball's Answer", value=f"{ballline}", inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Fun(bot))
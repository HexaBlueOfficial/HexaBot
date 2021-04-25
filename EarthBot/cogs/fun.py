import discord
import aiohttp
from discord.ext import commands, flags

class Fun(commands.Cog):
    """The cog for Earth's fun commands."""

    def __init__(self, bot):
        self.bot = bot
    
    def uwufy(self, sentence: str):
        uwu = sentence.lower()
        uwu = uwu.replace("l", "w")
        uwu = uwu.replace("r", "w")
        uwu = uwu.replace("th", "d")
        return f"{uwu}, uwu *rawr* XD!"
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> {sentence}"
    
    @flags.add_flag("-m", default="https://discord.gg/GFkEMD45xg")
    @flags.add_flag("--uwu", action="store_true")
    @flags.add_flag("-a", action="store_true")
    @flags.add_flag("-u", type=discord.User, default=None)
    @flags.add_flag("-c", type=discord.TextChannel, default=None)
    @flags.command(name="say")
    async def say(self, ctx, **flags):
        """The bot will say what you tell him to.\n\nFlags:\n`-m` - Message flag. Whatever you put after this flag and before the next flag will be the message repeated by the bot. If your message has more than a word, use quotation marks.\n`--uwu` - Turns your message into the UwU language.\n`-a` - Anonymization flag. Makes your message (`-m` flag content) anonymous.\n`-u` - User flag. Makes it look like another user sent your message (`-m` flag content). Works with username, username#discriminator, @mention and ID. Users outside this server will not work.\n`-c` - Channel flag. Sends the message in the channel you specify.\n\nExample command: `e.say -m "Insert cool message here." --uwu -a`.\nOutput: `insewt coow message hewe, uwu rawr XD!` (sent by Anonymous)."""

        if "@everyone" in flags["m"].lower():
            await ctx.author.send("Don't even try, idiot. You think I'm so stupid not to make a check?")
        if "@here" in flags["m"].lower():
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
        
        e = discord.Embed(title="Random Dog (from Random Fox by xinitrc)", color=0x00a8ff, description="Check out Random Fox [here](https://randomfox.ca)!")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_image(url=foxpic)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await fetching.edit(content=None, embed=e)

def setup(bot):
    bot.add_cog(Fun(bot))
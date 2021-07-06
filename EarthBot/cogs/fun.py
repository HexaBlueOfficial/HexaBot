import discord
import json
import aiohttp
import random
import asyncio
from discord.ext import commands

class SayFlags(commands.FlagConverter):
    """`e.say`'s Flags."""

    message: str = commands.flag(aliases=["m"], default="https://discord.gg/DsARcGwwdM")
    anonymous: bool = commands.flag(aliases=["a"], default=False)
    uwu: bool = commands.flag(default=False)
    user: discord.Member = commands.flag(aliases=["u"], default=None)

class PollView(discord.ui.View):
    """`e.poll`'s View."""

    def __init__(self, ctx: commands.Context, message: discord.Message, options: list, counts: list, timeout: float):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.message = message
        self.counts = counts
        for option in options:
            if option == options[0]:
                self.add_item(PollOption1(option, f"0\n{self.counts[0]}"))
            elif option == options[1]:
                self.add_item(PollOption2(option, f"1\n{self.counts[1]}"))
            else:
                try:
                    if option == options[2]:
                        self.add_item(PollOption3(option, f"2\n{self.counts[2]}"))
                except:
                    break
                else:
                    try:
                        if option == options[3]:
                            self.add_item(PollOption4(option, f"3\n{self.counts[3]}"))
                    except:
                        break
                    else:
                        try:
                            if option == options[4]:
                                self.add_item(PollOption5(option, f"4\n{self.counts[4]}"))
                        except:
                            break
                        else:
                            break
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)
    
    async def process_inputs(self, button: discord.ui.Button, interaction: discord.Interaction, count: str):
        if interaction.user.id == self.ctx.author.id:
            await interaction.response.send_message("The Poll author can't vote on their own Poll.", ephemeral=True)
        else:
            countx = count.splitlines()
            self.counts[countx[0]] = countx[1] + 1

            thing = 0
            for count in self.counts:
                thing += count
            
            operation = round((self.counts[countx[0]] * 100) / thing, 1)
            if str(operation).endswith(".0"):
                operation = round(operation)

            e = interaction.message.embeds[0]
            e.set_field_at(countx[0] + 1, value=f"{self.counts[countx[0]]} | {operation}%")
            await interaction.response.edit_message(embed=e)

class PollOption1(discord.ui.Button):
    """`e.poll`'s 1st Button."""

    view: PollView

    def __init__(self, option: str, count: str):
        super().__init__(style=discord.ButtonStyle.blurple, label=option, row=0)
        self.count = count
    
    async def callback(self, interaction: discord.Interaction):
        await self.view.process_inputs(self, interaction, self.count)

class PollOption2(discord.ui.Button):
    """`e.poll`'s 2nd Button."""

    view: PollView

    def __init__(self, option: str, count: str):
        super().__init__(style=discord.ButtonStyle.blurple, label=option, row=0)
        self.count = count
    
    async def callback(self, interaction: discord.Interaction):
        await self.view.process_inputs(self, interaction, self.count)

class PollOption3(discord.ui.Button):
    """`e.poll`'s 3rd Button."""

    view: PollView

    def __init__(self, option: str, count: str):
        super().__init__(style=discord.ButtonStyle.blurple, label=option, row=0)
        self.count = count
    
    async def callback(self, interaction: discord.Interaction):
        await self.view.process_inputs(self, interaction, self.count)

class PollOption4(discord.ui.Button):
    """`e.poll`'s 4th Button."""

    view: PollView

    def __init__(self, option: str, count: str):
        super().__init__(style=discord.ButtonStyle.blurple, label=option, row=0)
        self.count = count
    
    async def callback(self, interaction: discord.Interaction):
        await self.view.process_inputs(self, interaction, self.count)

class PollOption5(discord.ui.Button):
    """`e.poll`'s 5th Button."""

    view: PollView

    def __init__(self, option: str, count: str):
        super().__init__(style=discord.ButtonStyle.blurple, label=option, row=0)
        self.count = count
    
    async def callback(self, interaction: discord.Interaction):
        await self.view.process_inputs(self, interaction, self.count)

class HackView(discord.ui.View):
    """`e.hack`'s View."""

    def __init__(self, hacker: discord.User, hacked: discord.User):
        super().__init__()
        self.hacker = hacker
        self.hacked = hacked

    @discord.ui.button(label="Hack Discord", style=discord.ButtonStyle.blurple, row=0)
    async def hdiscord(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.hacker.id:
            e = interaction.message.embeds[0].description = "**DISCORD HACKED!**"
            await interaction.response.edit_message(embed=e)

            await interaction.response.send_message(f"Discord hacked successfully.\n(response to \"{button.label}\" Button click)", ephemeral=True)

            avatar = self.hacked.avatar.read()
            webhook = await interaction.channel.create_webhook(name=self.hacked.name, avatar=avatar, reason="Hack command.")

            await webhook.send("I got hacked, oh fuck.")
            await webhook.send(f"FUCK! {str(self.hacker)} HACKED ME!")

            await webhook.delete()

            for child in self.children:
                child.disabled = True
    
    @discord.ui.button(label="Hack YouTube", style=discord.ButtonStyle.red, row=0)
    async def hyoutube(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.hacker.id:
            e = interaction.message.embeds[0].description = "**YOUTUBE HACKED!**"
            await interaction.response.edit_message(embed=e)

            await interaction.response.send_message(f"YouTube hacked successfully.\n(response to \"{button.label}\" Button click)", ephemeral=True)

            avatar = self.hacked.avatar.read()
            webhook = await interaction.channel.create_webhook(name=self.hacked.name, avatar=avatar, reason="Hack command.")

            await webhook.send("I just posted a video!\nhttps://youtu.be/Blh2FCAIIgk")

            await webhook.delete()

            for child in self.children:
                child.disabled = True
    
    @discord.ui.button(label="Hack Twitter", style=discord.ButtonStyle.green, row=0)
    async def htwitter(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.hacker.id:
            e = interaction.message.embeds[0].description = "**TWITTER HACKED!**"
            await interaction.response.edit_message(embed=e)

            await interaction.response.send_message(f"Twitter hacked successfully.\n(response to \"{button.label}\" Button click)", ephemeral=True)

            avatar = self.hacked.avatar.read()
            webhook = await interaction.channel.create_webhook(name=self.hacked.name, avatar=avatar, reason="Hack command.")

            await webhook.send("I just tweeted!\nhttps://twitter.com/theEarthNet/status/1402642068200165383")

            await webhook.delete()

            for child in self.children:
                child.disabled = True

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
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> **{sentence}**"

    @commands.command(name="say")
    async def say(self, ctx: commands.Context, flags: SayFlags):
        """The bot will say what you tell it to.\n\nFlags:\n`message:` - Your message.\n`anonymous:` If the message has to be anonymised or not (`True`, `False`). Defaults to `False`.\n`uwu:` - If the message has to be UwUfied or not (`True`, `False`). Defaults to `False`.\n`user:` The member you want to \"steal the identity\" of, if you want to."""

        message = flags.message
        anonymous = flags.anonymous
        uwu = flags.uwu
        user = flags.user

        if anonymous:
            avatar = await self.bot.user.avatar.read()
            webhook = await ctx.channel.create_webhook(name="Anonymous", avatar=avatar, reason="Say command.")
        elif user is None:
            avatar = await ctx.author.avatar.read()
            webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=avatar, reason="Say command.")
        else:
            avatar = await user.avatar.read()
            webhook = await ctx.channel.create_webhook(name=user.name, avatar=avatar, reason="Say command.")
        
        if uwu:
            await webhook.send(self.uwufy(message))
        else:
            await webhook.send(message)
        await webhook.delete()
    
    @commands.command(name="uwu")
    async def uwu(self, ctx: commands.Context, *, sentence: str):
        """Reject English, evolve to Furry."""

        await ctx.message.reply(self.uwufy(sentence))
    
    @commands.command(name="cat")
    async def cat(self, ctx: commands.Context):
        """Shows a random image of a cat."""

        await ctx.trigger_typing()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search/") as response:
                cat = await response.json()
                catpic = cat[0]["url"]
        
        e = discord.Embed(title="Random Cat (from TheCatAPI by Aden)", color=int(self.embed["color"], 16), description="Check out TheCatAPI [here](https://thecatapi.com)!")
        e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
        e.set_image(url=catpic)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.message.reply(embed=e)
    
    @commands.command(name="dog")
    async def dog(self, ctx: commands.Context):
        """Shows a random image of a dog."""

        await ctx.trigger_typing()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thedogapi.com/v1/images/search/") as response:
                dog = await response.json()
                dogpic = dog[0]["url"]
        
        e = discord.Embed(title="Random Dog (from TheDogAPI by Aden)", color=int(self.embed["color"], 16), description="Check out TheDogAPI [here](https://thedogapi.com)!")
        e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
        e.set_image(url=dogpic)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.message.reply(embed=e)
    
    @commands.command(name="fox")
    async def fox(self, ctx: commands.Context):
        """Shows a random image of a fox."""

        await ctx.trigger_typing()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomfox.ca/floof/") as response:
                fox = await response.json()
                foxpic = fox["image"]
        
        e = discord.Embed(title="Random Fox (from Random Fox by xinitrc)", color=int(self.embed["color"], 16), description="Check out Random Fox [here](https://randomfox.ca)!")
        e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
        e.set_image(url=foxpic)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.message.reply(embed=e)

    @commands.command(name="hug")
    async def hug(self, ctx: commands.Context, member: discord.Member, *, message=None):
        """Hugs the user you want."""

        huglineint = random.randint(0, 9)
        halfpoint = self.huglines[str(huglineint)].replace("author", ctx.author.mention)
        hugline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Hug", color=int(self.embed["color"], 16), description=f"{hugline}")
        e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
        if message is not None:
            e.add_field(name=f"{ctx.author.name} included a message! They said...", value=f"{message}", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.message.reply(embed=e)
        await ctx.message.delete()
    
    @commands.command(name="kill")
    async def kill(self, ctx: commands.Context, member: discord.Member):
        """Kills the user you want."""

        killlineint = random.randint(0, 4)
        halfpoint = self.killlines[str(killlineint)].replace("author", ctx.author.mention)
        killline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Murder", color=int(self.embed["color"], 16), description=f"{killline}")
        e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.message.reply(embed=e)
    
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
            e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
            await ctx.message.reply(embed=e)
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
                e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
                e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                await ctx.message.reply(embed=e)
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
                e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
                e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                await ctx.message.reply(embed=e)
    
    @commands.command(name="8ball", aliases=["eightball"])
    async def eightball(self, ctx: commands.Context, *, question):
        """Seek an answer from the Magic 8 Ball."""

        balllineint = random.randint(0, 4)
        ballline = self.balllines[str(balllineint)]

        e = discord.Embed(title="Magic 8 Ball", color=int(self.embed["color"], 16))
        e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
        e.add_field(name="Your Question", value=f"{question}", inline=False)
        e.add_field(name="The 8 Ball's Answer", value=f"{ballline}", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.message.reply(embed=e)
    
    @commands.command(name="poll")
    async def poll(self, ctx: commands.Context, timeout: int=None):
        """Create a Poll."""

        initialise = await ctx.message.reply("What do you want the Poll's name to be?\n(You have 30 seconds.)")

        def check1(m):
            return m.author.id == ctx.author.id
        
        def check2(m):
            return m.author.id == ctx.author.id and len(m.content.split(" & ")) <= 5

        waitfor1 = await self.bot.wait_for("message", check=check1, timeout=30.0)
        e1 = await waitfor1.reply("What do you want your Poll's options to be?\nSplit them with space-ampersand-space (` & `). DON'T OMIT THE SPACES.\nMax options: 5.\nExample: `Very Sus & amog-uwu-s & Sussy Baka Amogus Impostor`\n(You have 2 minutes.)")
        waitfor2 = await self.bot.wait_for("message", check=check2, timeout=120.0)
        e2 = await waitfor2.reply(self.loading("Your Poll will be available soon..."))
        await asyncio.sleep(2.0)
        
        options = waitfor2.content.split(" & ")
        
        e = discord.Embed(title=f"Poll: {waitfor1.content}", color=int(self.embed["color"], 16), description=f"**Created by {ctx.author.mention}.**\nThink and give your answer.")
        e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])

        counts = []
        for option in options:
            e.add_field(name=option, value="0 | 0%", inline=False)
            counts.append(0)

        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])

        await ctx.message.delete()
        await initialise.delete()
        await waitfor1.delete()
        await e1.delete()
        await waitfor2.delete()
        await e2.delete()

        if timeout is not None:
            poll = await ctx.send(embed=e)
            await poll.edit(view=PollView(ctx, poll, options, counts, float(timeout)))
        else:
            await ctx.send(embed=e, view=PollView(ctx, options, counts, None))
    
    @commands.command(name="skittles", aliases=["skittleinfo", "skittlesinfo", "skittle"])
    async def skittles(self, ctx: commands.Context):
        """Gets info about a random Skittle.\nRequested by `skittlez#8168`."""

        await ctx.trigger_typing()

        skittleint = random.randint(0, 4)
        skittle = self.skittles[str(skittleint)]
        
        e = discord.Embed(title="Information about {} Skittle".format(skittle["color"]), color=int(self.embed["color"], 16))
        e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
        e.set_thumbnail(url=skittle["thumbnail"])
        e.add_field(name="Color", value=skittle["color"], inline=False)
        e.add_field(name="Flavor", value=skittle["flavor"], inline=False)
        e.add_field(name="Developer's Rating", value=skittle["devrate"], inline=False)
        e.add_field(name="Developer's Comment", value=skittle["devcomment"], inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.message.reply(embed=e)
    
    @commands.command(name="calculator", aliases=["calc"])
    async def calculator(self, ctx: commands.Context):
        """Soon..."""

        await ctx.message.reply("Soon...")
    
    @commands.command(name="hack")
    async def hack(self, ctx: commands.Context, user: discord.Member):
        """Hack a member (100% real)!"""

        hacking = await ctx.message.reply("<a:aLoading:833070225334206504> **Getting logins...**")
        await asyncio.sleep(1.0)
        await hacking.edit(content="<:Yes:833293078197829642> **Logins deciphered. Select what to hack below.**")
        
        e = discord.Embed(title=f"Hack {user.name}", color=int(self.embed["color"], 16), description=f"**Hacking {user.name} ready.**")
        e.set_author(name="{}".format(self.embed["authorname"] + "Fun"), icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await hacking.reply(embed=e, view=HackView(ctx.author, user))
            
def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
import discord
import discord_slash as slash
import json
import random
import platform
import asyncio
import aiohttp
from datetime import datetime
from discord_slash import cog_ext as slashcog
from discord.ext import commands

class TypeNotRecognised(Exception):
    pass

class Slash(commands.Cog):
    """Slash commands."""

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
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.launch_time = datetime.utcnow()
    
    @slashcog.cog_subcommand(base="info", name="bot", description="Shows information about the Earth bot.")
    async def _bot(self, ctx: slash.SlashContext):
        luckyint = random.randint(1, 20)
        
        e = discord.Embed(title="About Earth", color=int(self.embed["color"], 16), description="**Earth** is a private bot for the server **Planet Earth**. It has a few fun commands to keep you entertained while it also does more serious stuff.")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Developers", value="<@450678229192278036>: All commands.\n<@598325949808771083>: `/help`.\nOther: `/jishaku` (External Extension).", inline=False)
        e.add_field(name="Versions", value=f"Python Earth: v1.4.1\nPython: v{platform.python_version()}\ndiscord.py: v{discord.__version__}", inline=False)
        e.add_field(name="Credits", value="**Hosting:** [Library of Code](https://loc.sh/discord)\n**Inspiration for `/kill`, `/hack`, `/gaypercent` and `/8ball`:** [Dank Memer](https://dankmemer.lol) bot.\n**Inspiration for `/uwu`:** [Reddit UwUtranslator bot](https://reddit.com/u/uwutranslator)\n**Cats:** [TheCatAPI](https://thecatapi.com)\n**Dogs:** [TheDogAPI](https://thedogapi.com)\n**Foxes:** [Random Fox](https://randomfox.ca)", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        infomessage = await ctx.send(embed=e, components=[
            slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "Invite", None, "invite"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Support", None, None, "https://discord.gg/DsARcGwwdM")
            )
        ])

        if luckyint == 8:
            await ctx.author.send("Hey!")
            await ctx.author.send("You should try running `e.arth`!")
        
        while 0 == 0:
            waitfor = await slash.utils.manage_components.wait_for_component(self.bot, infomessage, "invite")
            await waitfor.send("**Coming soon...**", hidden=True)
    
    @slashcog.cog_slash(name="guilds", description="You found a Developer command!\nThere's a good chance you can't use this.", guild_ids=[832594030264975420], options=[
        slash.utils.manage_commands.create_option("datatype", "Data to find.", 3, True, choices=[
            slash.utils.manage_commands.create_choice("all", "Everything"),
            slash.utils.manage_commands.create_choice("name", "Guild Names"),
            slash.utils.manage_commands.create_choice("id", "Guild IDs"),
            slash.utils.manage_commands.create_choice("owner", "Guild Owners' Username and Discriminator"),
            slash.utils.manage_commands.create_choice("invite", "Guild Invites")
        ])
    ], default_permission=False, permissions={
        832594030264975420: [
            slash.utils.manage_commands.create_permission(450678229192278036, slash.utils.manage_commands.SlashCommandPermissionType.USER, True)
        ],
        838718002412912661: [
            slash.utils.manage_commands.create_permission(450678229192278036, slash.utils.manage_commands.SlashCommandPermissionType.USER, True)
        ]
    })
    async def _guilds(self, ctx: slash.SlashContext, datatype: str):
        typex = datatype
        
        data = f""
        for guild in self.bot.guilds:
            if typex == "name":
                data += f"{guild.name}\n"
            elif typex == "id":
                data += f"{guild.id}\n"
            elif typex == "owner":
                data += f"{str(guild.owner)}\n"
            elif typex == "invite":
                invite = await guild.text_channels[0].create_invite(reason="Developer \"Guilds\" Command", max_uses=3)
                data += f"{invite.url}\n"
            elif typex == "all":
                invite = await guild.text_channels[0].create_invite(reason="Developer \"Guilds\" Command", max_uses=3)
                data += f"{guild.name} | {guild.id} | {str(guild.owner)} | {invite.url}\n"
            else:
                raise TypeNotRecognised
        data = data.rstrip()
        
        e = discord.Embed(title=f"Guilds [type=\"{typex}\"]", color=int(self.embed["color"], 16), description=data)
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="getupdates", description="Get updates about the Earth!", options=[
        slash.utils.manage_commands.create_option("updates", "The updates you want.", 3, True, choices=[
            slash.utils.manage_commands.create_choice("832660792397791262", "Global Warming Updates"),
            slash.utils.manage_commands.create_choice("832661047398760450", "Endangered Species Updates"),
            slash.utils.manage_commands.create_choice("832671013753454602", "Evil Companies Updates")
        ]),
        slash.utils.manage_commands.create_option("to", "The channel to get the news at.", 3, True)
    ])
    @commands.has_guild_permissions(manage_guild=True)
    async def _getupdates(self, ctx: slash.SlashContext, updates: str, to: str):
        earthnet = self.bot.get_guild(832594030264975420)
        tofollow = earthnet.get_channel(int(updates))
        try:
            to = int(to)
        except:
            to = to.lstrip("<#")
            to = to.rstrip(">")
            to = int(to)
        to = ctx.guild.get_channel(to)
        await tofollow.follow(destination=to, reason="GetUpdates command.")

        followed = ""
        if updates == "832660792397791262":
            followed = "Global Warming Updates"
        elif updates == "832661047398760450":
            followed = "Endangered Species Updates"
        elif updates == "832671013753454602":
            followed = "Evil Companies Updates"
        await ctx.send(f"Successfully followed {followed}.")
    
    @slashcog.cog_slash(name="fundraiser", description="This command gets updated everytime a new Fundraiser starts in the EarthNetwork server.")
    async def _fundraiser(self, ctx: slash.SlashContext):
        e = discord.Embed(title="How to donate to WWF", color=int(self.embed["color"], 16), description="**How to donate to WWF:**\n\n**Step 1:** Go to https://worldwildlife.org (WWF's official website).\n**Step 2:** Hover over the big, red, \"DONATE\" button.\n**Step 3:** Select \"Make a One-time Donation\" from the dropdown.\n**Step 4:** Select what you prefer and enter your info.\n**Step 5:** Press \"Submit\".\n\nCongratulations: you helped our Planet!")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="say", description="The bot will say what you tell it to.", options=[
        slash.utils.manage_commands.create_option("message", "Whatever you type after this option will be what is going to be said.", 3, False), 
        slash.utils.manage_commands.create_option("anonymous", "Include this to make your message anonymous.", 5, False),
        slash.utils.manage_commands.create_option("uwu", "Include this to turn your message to UwU.", 5, False),
        slash.utils.manage_commands.create_option("channel", "Include this to send your message in a channel that isn't the Context channel.", 7, False),
        slash.utils.manage_commands.create_option("user", "Include this to send the message as another user.", 6, False)
        ])
    async def _say(self, ctx: slash.SlashContext, message="https://discord.gg/DsARcGwwdM", anonymous=False, uwu=False, channel=None, user=None):
        words = ["@everyone", "@here", "<@&832657099312857124>"]
        for word in words:
            if word in message.lower():
                await ctx.author.send("Don't even try, idiot. You think I'm so stupid not to make a check?")
        
        if anonymous:
            if channel is None:
                avatar = await self.bot.user.avatar_url.read()
                webhook = await ctx.channel.create_webhook(name="Anonymous", avatar=avatar, reason="Say command.")
            else:
                avatar = await self.bot.user.avatar_url.read()
                webhook = await channel.create_webhook(name="Anonymous", avatar=avatar, reason="Say command.")
        elif user is not None:
            if channel is None:
                avatar = await user.avatar_url.read()
                webhook = await ctx.channel.create_webhook(name=user.name, avatar=avatar, reason="Say command.")
            else:
                avatar = await user.avatar_url.read()
                webhook = await channel.create_webhook(name=user.name, avatar=avatar, reason="Say command.")
        else:
            if channel is None:
                avatar = await ctx.author.avatar_url.read()
                webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=avatar, reason="Say command.")
            else:
                avatar = await ctx.author.avatar_url.read()
                webhook = await channel.create_webhook(name=ctx.author.name, avatar=avatar, reason="Say command.")

        if not uwu:
            await webhook.send(message)
        else:
            await webhook.send(self.uwufy(message))
        await webhook.delete()
        await ctx.send("Successfully executed command!", hidden=True)
    
    @slashcog.cog_slash(name="uwu", description="Reject English, evolve to Furry.", options=[
        slash.utils.manage_commands.create_option("sentence", "This is what will be turned into the UwU language.", 3, True)
    ])
    async def _uwu(self, ctx: slash.SlashContext, sentence):
        await ctx.send(self.uwufy(sentence))
    
    @slashcog.cog_slash(name="cat", description="Shows a random image of a cat.")
    async def _cat(self, ctx: slash.SlashContext):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search/") as response:
                cat = await response.json()
                catpic = cat[0]["url"]
        
        e = discord.Embed(title="Random Cat (from TheCatAPI by Aden)", color=int(self.embed["color"], 16), description="Check out TheCatAPI [here](https://thecatapi.com)!")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_image(url=catpic)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="dog", description="Shows a random image of a dog.")
    async def _dog(self, ctx: slash.SlashContext):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thedogapi.com/v1/images/search/") as response:
                dog = await response.json()
                dogpic = dog[0]["url"]
        
        e = discord.Embed(title="Random Dog (from TheDogAPI by Aden)", color=int(self.embed["color"], 16), description="Check out TheDogAPI [here](https://thedogapi.com)!")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_image(url=dogpic)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="fox", description="Shows a random image of a fox.")
    async def _fox(self, ctx: slash.SlashContext):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomfox.ca/floof/") as response:
                fox = await response.json()
                foxpic = fox["image"]
        
        e = discord.Embed(title="Random Fox (from Random Fox by xinitrc)", color=int(self.embed["color"], 16), description="Check out Random Fox [here](https://randomfox.ca)!")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_image(url=foxpic)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="hug", description="Hugs the user you want.", options=[
        slash.utils.manage_commands.create_option("member", "The user you want to hug. You can select from the popup list, type their username, or their ID.", 6, True),
        slash.utils.manage_commands.create_option("message", "Something you'd like to tell who you just hugged, for example why you decided to do so.", 3, False)
    ])
    async def _hug(self, ctx: slash.SlashContext, member, message=None):
        huglineint = random.randint(0, 9)
        halfpoint = self.huglines[str(huglineint)].replace("author", ctx.author.mention)
        hugline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Hug", color=int(self.embed["color"], 16), description=f"{hugline}")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        if message is not None:
            e.add_field(name=f"{ctx.author.name} included a message! They said...", value=f"{message}", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="kill", description="Kills the user you want.", options=[
        slash.utils.manage_commands.create_option("member", "The user you want to kill. You can select from the popup list, type their username, or their ID.", 6, True)
    ])
    async def _kill(self, ctx: slash.SlashContext, member):
        killlineint = random.randint(0, 4)
        halfpoint = self.killlines[str(killlineint)].replace("author", ctx.author.mention)
        killline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Murder", color=int(self.embed["color"], 16), description=f"{killline}")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="gaypercent", description="Wanna find out how gay something is? This command is for you.", options=[
        slash.utils.manage_commands.create_option("thing", "The thing you want to see the gay% of. Can be a user.", 3, False)
    ])
    async def _gaypercent(self, ctx: slash.SlashContext, thing=None):
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
    
    @slashcog.cog_slash(name="8ball", description="Seek an answer from the Magic 8 Ball.", options=[
        slash.utils.manage_commands.create_option("question", "What you want to ask the Magic 8 Ball.", 3, True)
    ])
    async def _eightball(self, ctx: slash.SlashContext, question):
        balllineint = random.randint(0, 4)
        ballline = self.balllines[str(balllineint)]

        e = discord.Embed(title="Magic 8 Ball", color=int(self.embed["color"], 16))
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.add_field(name="Your Question", value=f"{question}", inline=False)
        e.add_field(name="The 8 Ball's Answer", value=f"{ballline}", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="poll", description="Create a poll. Currently only supports two options.", options=[
        slash.utils.manage_commands.create_option("name", "The poll's name.", 3, True),
        slash.utils.manage_commands.create_option("option1", "The first option to vote on.", 3, True),
        slash.utils.manage_commands.create_option("option2", "The second option to vote on.", 3, True)
    ])
    async def _poll(self, ctx: slash.SlashContext, name: str, option1: str, option2: str):
        vote1 = 0
        vote2 = 0
        
        e = discord.Embed(title=f"Poll: {name}", color=int(self.embed["color"], 16), description=f"**Poll by {ctx.author.mention}.**\nThink and choose.")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.add_field(name=option1, value=f"{vote1}")
        e.add_field(name=option2, value=f"{vote2}")
        e.add_field(name="Percentages", value=f"{option1}: 0%\n{option2}: 0%", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        pollmessage = await ctx.send(embed=e, components=[
            slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "1st Option", None, "opt1"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "2nd Option", None, "opt2")
            )
        ])

        while 0 == 0:
            waitfor = await slash.utils.manage_components.wait_for_component(self.bot, pollmessage, ["opt1", "opt2"])
            e.clear_fields()
            if waitfor.custom_id == "opt1":
                vote1 += 1
            elif waitfor.custom_id == "opt2":
                vote2 += 1
            operation1 = round((vote1 * 100) / (vote1 + vote2), 1)
            operation2 = round((vote2 * 100) / (vote1 + vote2), 1)
            if str(operation1).endswith(".0"):
                operation1 = round(operation1)
            if str(operation2).endswith(".0"):
                operation2 = round(operation2)
            e.add_field(name=option1, value=f"{vote1}")
            e.add_field(name=option2, value=f"{vote2}")
            e.add_field(name="Percentages", value=f"{option1}: {operation1}%\n{option2}: {operation2}%")
            await waitfor.edit_origin(embed=e)
        
    @slashcog.cog_slash(name="skittles", description="Gets info about a random Skittle.\nRequested by `skittlez#8168`.")
    async def _skittles(self, ctx: slash.SlashContext):
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
    
    @slashcog.cog_slash(name="calculator", description="Calculate.")
    async def _calculator(self, ctx: slash.SlashContext):
        string = ""

        e = discord.Embed(title=f"{ctx.author.name}'s Calculator", color=int(self.embed["color"], 16), description="```\n \n```")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        calculatormessage = await ctx.send(embed=e, components=[
            slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "7", None, "7"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "8", None, "8"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "9", None, "9"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "+", None, "+"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.red, "Close", None, "exit")
            ),
            slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "4", None, "4"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "5", None, "5"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "6", None, "6"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "-", None, "-"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.red, "←", None, "back")
            ),
            slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "1", None, "1"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "2", None, "2"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "3", None, "3"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "*", None, "*"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.red, "Clear", None, "clear")
            ),
            slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "00", None, "00"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "0", None, "0"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, ".", None, "."),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "/", None, "/"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.green, "=", None, "=")
            )
        ])

        async def check1(string):
            try:
                if string.split("|")[-2] == "+":
                    return False
                elif string.split("|")[-2] == "-":
                    return False
                elif string.split("|")[-2] == "*":
                    return False
                elif string.split("|")[-2] == "/":
                    return False
            except:
                return True
            else:
                return False
        
        async def check2(string):
            try:
                if string.split("|")[-2] == "+":
                    return False
                elif string.split("|")[-2] == "-":
                    return False
                elif string.split("|")[-2] == "*":
                    return False
                elif string.split("|")[-2] == "/":
                    return False
                elif "+" in string.split("|"):
                    return False
                elif "-" in string.split("|"):
                    return False
                elif "*" in string.split("|"):
                    return False
                elif "/" in string.split("|"):
                    return False
            except:
                return True
            else:
                return False
        
        while 0 == 0:
            waitfor = await slash.utils.manage_components.wait_for_component(self.bot, calculatormessage, ["00", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "=", "exit", "back", "clear"])
            if waitfor.author.id == ctx.author.id:
                try:
                    int(waitfor.custom_id)
                except:
                    if waitfor.custom_id == "exit":
                        e.description = "```\nThis Calculator has been closed.\n```"
                        await waitfor.edit_origin(embed=e)
                        await calculatormessage.edit(components=[
                            slash.utils.manage_components.create_actionrow(
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "7", None, "7", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "8", None, "8", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "9", None, "9", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "+", None, "+", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.red, "Close", None, "exit", None, True)
                            ),
                            slash.utils.manage_components.create_actionrow(
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "4", None, "4", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "5", None, "5", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "6", None, "6", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "-", None, "-", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.red, "←", None, "back", None, True)
                            ),
                            slash.utils.manage_components.create_actionrow(
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "1", None, "1", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "2", None, "2", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "3", None, "3", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "*", None, "*", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.red, "Clear", None, "clear", None, True)
                            ),
                            slash.utils.manage_components.create_actionrow(
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "00", None, "00", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "0", None, "0", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, ".", None, ".", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "/", None, "/", None, True),
                                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.green, "=", None, "=", None, True)
                            )
                            ])
                        await waitfor.send("Calculator closed.", hidden=True)
                        break
                    elif waitfor.custom_id == "back":
                        stringx = list(string).pop()
                        string = ""
                        for character in stringx:
                            string += character
                        stringe = string.replace("|", "")
                        e.description = f"```\n{stringe}\n```"
                        await waitfor.edit_origin(embed=e)
                    elif waitfor.custom_id == "clear":
                        string = ""
                        e.description = f"```\n \n```"
                        await waitfor.edit_origin(embed=e)
                    elif waitfor.custom_id == "=":
                        stringx = string.split("|")
                        operation = 0
                        if stringx[1] == "+":
                            operation = float(stringx[0]) + float(stringx[2])
                        elif stringx[1] == "-":
                            operation = float(stringx[0]) - float(stringx[2])
                        elif stringx[1] == "*":
                            operation = float(stringx[0]) * float(stringx[2])
                        elif stringx[1] == "/":
                            operation = float(stringx[0]) / float(stringx[2])
                        if str(operation).endswith(".0"):
                            operation = int(operation)
                        string = f"{operation}"
                        e.description = f"```\n{string}\n```"
                        await waitfor.edit_origin(embed=e)
                    elif waitfor.custom_id == "+":
                        if await check2(string):
                            string += "|+|"
                            stringe = string.replace("|", "")
                            e.description = f"```\n{stringe}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                    elif waitfor.custom_id == "-":
                        if await check2(string):
                            string += "|-|"
                            stringe = string.replace("|", "")
                            e.description = f"```\n{stringe}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                    elif waitfor.custom_id == "*":
                        if await check2(string):
                            string += "|*|"
                            stringe = string.replace("|", "")
                            e.description = f"```\n{stringe}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                    elif waitfor.custom_id == "/":
                        if await check2(string):
                            string += "|/|"
                            stringe = string.replace("|", "")
                            e.description = f"```\n{stringe}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                    elif waitfor.custom_id == ".":
                        if check1(string):
                            string += waitfor.custom_id
                            e.description = f"```\n{string}\n```"
                            await waitfor.edit_origin(embed=e)
                        else:
                            await waitfor.send("**This interaction failed.**", hidden=True)
                else:
                    string += waitfor.custom_id
                    stringe = string.replace("|", "")
                    e.description = f"```\n{stringe}\n```"
                    await waitfor.edit_origin(embed=e)
    
    @slashcog.cog_slash(name="hack", description="Hack a member (100% real)!", options=[
        slash.utils.manage_commands.create_option("user", "The member to hack.", 6, True)
    ])
    async def _hack(self, ctx: slash.SlashContext, user: discord.Member):
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
    
    @slashcog.cog_slash(name="tictactoe", description="Play Tic-Tac-Toe!")
    async def _tictactoe(self, ctx: slash.SlashContext):
        await ctx.send("**Coming soon...**", hidden=True)

#        e = discord.Embed(title="Tic-Tac-Toe", color=self.embed["color"], description="Play below.")
#        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
#        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
#        tttmessage = await ctx.send(embed=e, components=[
#            slash.utils.manage_components.create_actionrow(
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "0.0"),
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "0.1"),
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "0.2")
#            ),
#            slash.utils.manage_components.create_actionrow(
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "1.0"),
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "1.1"),
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "1.2")
#            ),
#            slash.utils.manage_components.create_actionrow(
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "2.0"),
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "2.1"),
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "2.2")
#            )
#        ])

#        waitfor = await slash.utils.manage_components.wait_for_component(self.bot, tttmessage, ["0.0", "0.1", "0.2", "1.0", "1.1", "1.2", "2.0", "2.1", "2.2"])
#        if waitfor.author.id == ctx.author.id:
#            if waitfor.custom_id == "0.0":
#                await tttmessage.edit(components=[
#                    slash.utils.manage_components.create_actionrow(
#                    slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "", None, "0.0"),
#                    slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "0.1"),
#                    slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "0.2")
#                    ),
#                    slash.utils.manage_components.create_actionrow(
#                        slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "1.0"),
#                        slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "1.1"),
#                        slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "1.2")
#                    ),
#                    slash.utils.manage_components.create_actionrow(
#                        slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "2.0"),
#                        slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "2.1"),
#                        slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.grey, "", None, "2.2")
#                    )
#                ])
    
    @slashcog.cog_slash(name="uptime", description="Shows an Embed with Earth's uptime.")
    async def _uptime(self, ctx: slash.SlashContext):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        e = discord.Embed(title="Uptime", color=int(self.embed["color"], 16), description=f"The bot has been online for:\n{days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.add_field(name="Last Restart", value="The bot was last restarted on {} UTC".format(self.bot.launch_time.strftime("%A, %d %B %Y at %H:%M")), inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="ping", description="Shows an Embed with Earth's ping latency.")
    async def _ping(self, ctx: slash.SlashContext):
        ping = self.bot.latency * 1000
        pingr = round(ping, 1)
        e = discord.Embed(title="Ping Latency", color=int(self.embed["color"], 16), description=f"My ping latency is {pingr}ms. It's the time it takes for my host's servers to reach Discord.")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_subcommand(base="info", name="user", description="Retrieves information about a user.", options=[
        slash.utils.manage_commands.create_option("user", "The user to find.", 3, False)
    ])
    async def _user(self, ctx: slash.SlashContext, user=None):
        if user is None:
            string = ""
            for role in ctx.author.roles:
                if role == ctx.guild.default_role:
                    continue
                string = string + f"{role.mention} "

            e = discord.Embed(title=f"Information for {str(ctx.author)}", color=int(self.embed["color"], 16))
            e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
            e.set_thumbnail(url=ctx.author.avatar_url)
            e.add_field(name="Username", value=f"{ctx.author.name}")
            e.add_field(name="Discriminator", value=f"{ctx.author.discriminator}")
            e.add_field(name="ID", value=f"{ctx.author.id}")
            if ctx.author.nick is not None:
                e.add_field(name="Nickname", value=f"{ctx.author.nick}")
            e.add_field(name="Status", value=f"{ctx.author.status}")
            if ctx.author.activity is not None:
                e.add_field(name="Activity", value=f"{ctx.author.activity}")
            e.add_field(name="Color", value=f"{ctx.author.color}")
            e.add_field(name="Joined At", value="{} UTC".format(ctx.author.joined_at.strftime("%A, %d %B %Y at %H:%M")))
            e.add_field(name="Created At", value="{} UTC".format(ctx.author.created_at.strftime("%A, %d %B %Y at %H:%M")))
            e.add_field(name="Roles", value=string)
            e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
            await ctx.send(embed=e)
        else:
            try:
                user = int(user)
            except:
                user = str(user).lstrip("<@!")
                user = user.rstrip(">")
                user = int(user)

                user = self.bot.get_user(user)

                if user in ctx.guild.members:
                    user = ctx.guild.get_member(user.id)

                string = ""
                for role in user.roles:
                    if role == ctx.guild.default_role:
                        continue
                    string = string + f"{role.mention} "

                e = discord.Embed(title=f"Information for {str(user)}", color=int(self.embed["color"], 16))
                e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
                e.set_thumbnail(url=user.avatar_url)
                e.add_field(name="Username", value=f"{user.name}")
                e.add_field(name="Discriminator", value=f"{user.discriminator}")
                e.add_field(name="ID", value=f"{user.id}")
                if user.nick is not None:
                    e.add_field(name="Nickname", value=f"{user.nick}")
                e.add_field(name="Status", value=f"{user.status}")
                if user.activity is not None:
                    e.add_field(name="Activity", value=f"{user.activity}")
                e.add_field(name="Color", value=f"{user.color}")
                e.add_field(name="Joined At", value="{} UTC".format(user.joined_at.strftime("%A, %d %B %Y at %H:%M")))
                e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")))
                e.add_field(name="Roles", value=string)
                e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                await ctx.send(embed=e)
            else:
                user = await self.bot.fetch_user(user)

                if user in ctx.guild.members:
                    user = ctx.guild.get_member(user.id)

                    string = ""
                    for role in user.roles:
                        if role == ctx.guild.default_role:
                            continue
                        string = string + f"{role.mention} "

                    e = discord.Embed(title=f"Information for {str(user)}", color=int(self.embed["color"], 16))
                    e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
                    e.set_thumbnail(url=user.avatar_url)
                    e.add_field(name="Username", value=f"{user.name}")
                    e.add_field(name="Discriminator", value=f"{user.discriminator}")
                    e.add_field(name="ID", value=f"{user.id}")
                    if user.nick is not None:
                        e.add_field(name="Nickname", value=f"{user.nick}")
                    e.add_field(name="Status", value=f"{user.status}")
                    if user.activity is not None:
                        e.add_field(name="Activity", value=f"{user.activity}")
                    e.add_field(name="Color", value=f"{user.color}")
                    e.add_field(name="Joined At", value="{} UTC".format(user.joined_at.strftime("%A, %d %B %Y at %H:%M")))
                    e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")))
                    e.add_field(name="Roles", value=string)
                    e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                    await ctx.send(embed=e)
                else:
                    e = discord.Embed(title=f"Information for {str(user)}", color=int(self.embed["color"], 16))
                    e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
                    e.set_thumbnail(url=user.avatar_url)
                    e.add_field(name="Username", value=f"{user.name}")
                    e.add_field(name="Discriminator", value=f"{user.discriminator}")
                    e.add_field(name="ID", value=f"{user.id}")
                    e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")))
                    e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
                    await ctx.send(embed=e)
    
    @slashcog.cog_subcommand(base="info", name="server", description="Shows information about the Context Guild.")
    async def _server(self, ctx: slash.SlashContext):
        memberCount = 0
        botCount = 0
        for member in ctx.guild.members:
            if member.bot:
                botCount = botCount + 1
            else:
                memberCount = memberCount + 1
            
        string = ""
        for role in ctx.guild.roles:
            if role == ctx.guild.default_role:
                continue
            if role.name == "‎‎‎‎":
                continue
            string = string + f"{role.mention} "
            
        e = discord.Embed(title=f"Information for {ctx.guild.name}", color=int(self.embed["color"], 16))
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_thumbnail(url=ctx.guild.icon_url)
        e.add_field(name="Name", value=f"{ctx.guild.name}")
        e.add_field(name="Owner", value=f"{str(ctx.guild.owner)}")
        e.add_field(name="ID", value=f"{ctx.guild.id}")
        e.add_field(name="User Count", value=f"{len(ctx.guild.members)}")
        e.add_field(name="Member Count", value=f"{memberCount}")
        e.add_field(name="Bot Count", value=f"{botCount}")
        e.add_field(name="Emojis", value=f"{len(ctx.guild.emojis)}")
        e.add_field(name="Created At", value="{} UTC".format(ctx.guild.created_at.strftime("%A, %d %B %Y at %H:%M")))
        e.add_field(name="Roles", value=string)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)
    
    @slashcog.cog_subcommand(base="info", name="emoji", description="Shows information about an Emoji in this server.", options=[
        slash.utils.manage_commands.create_option("emoji", "The emoji's name.", 3, True)
    ])
    async def _emoji(self, ctx: slash.SlashContext, emoji: str):
        await ctx.send("<:No:833293106198872094> This command is broken at the moment.")

#       emoji = discord.utils.get(ctx.guild.emojis, name=emoji)

#        e = discord.Embed(title=f"Information about {emoji.name}", color=int(self.embed["color"], 16))
#        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
#        e.set_thumbnail(url=emoji.url)
#        e.add_field(name="Name", value=f"{emoji.name}")
#        e.add_field(name="ID", value=f"{emoji.id}")
#        e.add_field(name="Animated", value=f"{emoji.animated}")
#        e.add_field(name="Created At", value="{} UTC".format(emoji.created_at.strftime("%A, %d %B %Y at %H:%M")))
#        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
#        await ctx.send(embed=e, components=[
#            slash.utils.manage_components.create_actionrow(
#                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "Use Emoji", emoji, "use")
#            )
#        ])

#        waitfor = await self.bot.wait_for("component", check=lambda ctx: ctx.custom_id == "use")
#        if waitfor.author_id == ctx.author.id:
#            componentbug = await waitfor.send("Emoji used successfully!", hidden=True)
#            await self._nitro(ctx, emoji.name)
#            await asyncio.sleep(1.0)
#            await componentbug.delete()
    
    @slashcog.cog_subcommand(base="discord", name="servers", description="Discord's Official servers.")
    async def _servers(self, ctx: slash.SlashContext):
        luckyint = random.randint(1, 10)

        if luckyint == 8:
            components = slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Join Discord Testers", None, None, "https://discord.gg/discord-testers"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Join Discord Townhall", None, None, "https://discord.gg/discord-townhall"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Join Discord Developers", None, None, "https://discord.gg/discord-developers"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Join quikblend", None, None, "https://discord.gg/quikblend")
            )
        else:
            components = slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Join Discord Testers", None, None, "https://discord.gg/discord-testers"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Join Discord Townhall", None, None, "https://discord.gg/discord-townhall"),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Join Discord Developers", None, None, "https://discord.gg/discord-developers")
            )

        e = discord.Embed(title="Discord's Official Servers", color=int(self.embed["color"], 16))
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.add_field(name="Discord Testers", value="The official place to report Discord Bugs! Help find bugs, chat with others and be a part of the testers community!", inline=False)
        e.add_field(name="Discord Townhall", value="Discord is your place to talk. Talk with other users, share your latest adventures and make some new ones.", inline=False)
        e.add_field(name="Discord Developers (previously GameSDK)", value="A place to discuss Discord's API and SDKs with community developers and Discord staff alike!", inline=False)
        if luckyint == 8:
            e.add_field(name="quikblend", value="No official description.\nAn official Discord Staff's server.", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e, components=[components])
    
    @slashcog.cog_subcommand(base="discord", name="downloads", description="Download links for all Desktop editions.", options=[
        slash.utils.manage_commands.create_option("os", "The Operating System you use and the installer file format.", 3, True, choices=[
            slash.utils.manage_commands.create_choice("win", "Windows (.exe)"),
            slash.utils.manage_commands.create_choice("mac", "macOS (.dmg)"),
            slash.utils.manage_commands.create_choice("tar", "Linux (.tar.gz)"),
            slash.utils.manage_commands.create_choice("deb", "Linux (.deb)")
        ])
    ])
    async def _downloads(self, ctx: slash.SlashContext, os: str):
        links = []
        if os == "win":
            links = ["https://discord.com/api/download?platform=win", "https://discord.com/api/download/ptb?platform=win", "https://discord.com/api/download/canary?platform=win", "https://discord.com/api/download/development?platform=win"]
        elif os == "mac":
            links = ["https://discord.com/api/download?platform=osx", "https://discord.com/api/download/ptb?platform=osx", "https://discord.com/api/download/canary?platform=osx", "https://discord.com/api/download/development?platform=osx"]
        elif os == "tar":
            links = ["https://discord.com/api/download?platform=linux&format=tar.gz", "https://discord.com/api/download/ptb?platform=linux&format=tar.gz", "https://discord.com/api/download/canary?platform=linux&format=tar.gz", "https://discord.com/api/download/development?platform=linux&format=tar.gz"]
        elif os == "deb":
            links = ["https://discord.com/api/download?platform=linux&format=deb", "https://discord.com/api/download/ptb?platform=linux&format=deb", "https://discord.com/api/download/canary?platform=linux&format=deb", "https://discord.com/api/download/development?platform=linux&format=deb"]
        
        e = discord.Embed(title="Discord's Downloads", color=int(self.embed["color"], 16))
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.add_field(name="Stable", value="The most popular edition of Discord. You'll almost never find a bug on this one.\nMISSING ESSENTIAL FEATURE: Ability to see Component type \"Select\" (dropdown menus).", inline=False)
        e.add_field(name="Public Test Build (PTB)", value="This edition can be called Beta. It is possible to find bugs on this one.", inline=False)
        e.add_field(name="Canary", value="This editon is basically an Alpha: you get the newest features. It is likely you'll find bugs on this one.", inline=False)
        e.add_field(name="Development", value="This edition is used by the very Discord Staff for testing. Very high risk of encountering bugs.\nMISSING ESSENTIAL FEATURE: Ability to report bugs in [Discord Testers](https://discord.gg/discord-testers). Reports on Development will immediately be denied.", inline=False)
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e, components=[
            slash.utils.manage_components.create_actionrow(
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Download Stable", None, None, links[0]),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Download PTB", None, None, links[1]),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Download Canary", None, None, links[2]),
                slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.URL, "Download Development", None, None, links[3])
            )
        ])
    
    @slashcog.cog_slash(name="nitro", description="Sends animated emojis (from this server) with your name.", options=[
        slash.utils.manage_commands.create_option("emoji", "The emoji's name.", 3, True)
    ])
    async def _nitro(self, ctx: slash.SlashContext, emoji: str):
        await ctx.send("<:No:833293106198872094> This command is broken at the moment.")

#        emoji = discord.utils.get(ctx.guild.emojis, name=emoji)

#        avatar = await ctx.author.avatar_url.read()
#        webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=avatar, reason="Nitro command.")

#        await webhook.send(f"<a:{emoji.name}:{emoji.id}>")
#        slashbug = await ctx.send("Command executed successfully!")
#        await slashbug.delete()
#        await webhook.delete()

def setup(bot: commands.Bot):
    bot.add_cog(Slash(bot))

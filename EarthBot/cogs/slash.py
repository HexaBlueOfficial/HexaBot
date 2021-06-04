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
        with open("./Earth/EarthBot/misc/hug.json") as hugs:
            self.huglines = json.load(hugs)
        with open("./Earth/EarthBot/misc/kill.json") as kills:
            self.killlines = json.load(kills)
        with open("./Earth/EarthBot/misc/gay.json") as gays:
            self.gaylines = json.load(gays)
        with open("./Earth/EarthBot/misc/8ball.json") as eightballs:
            self.balllines = json.load(eightballs)
        with open("./token.json") as tokenfile:
            tokendict = json.load(tokenfile)
        self.token = tokendict["token"]
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> **{sentence}**"
    
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
    
    @slashcog.cog_slash(name="info", description="Shows information about Earth.")
    async def _info(self, ctx: slash.SlashContext):
        luckyint = random.randint(1, 100)
        
        e = discord.Embed(title="About Earth", color=0x00a8ff, description="**Earth** is a private bot for the server **Planet Earth**. It has a few fun commands to keep you entertained while it also does more serious stuff.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Developers", value="<@450678229192278036>: `/info`, AutoPublish, AutoPing, `/say`, `/uwu`, `/cat`, `/dog`, `/fox`, `/hug`, `/kill`, `/gaypercent`, `/8ball`, `/poll`, `/ping`, `/uptime`, `/userinfo`, `/serverinfo`, `/nitro`.\n<@598325949808771083>: `/help`.\nOther: `/jishaku` (External Extension).", inline=False)
        if luckyint == 69:
            e.set_field_at(0, name="Developers", value="<@450678229192278036>: `/info`, AutoPublish, AutoPing, `e.arth`, `/say`, `/uwu`, `/cat`, `/dog`, `/fox`, `/hug`, `/kill`, `/gaypercent, `/8ball`, `/poll`, `/ping`, `/uptime`, `/userinfo`, `/serverinfo`, `/nitro`.\n<@598325949808771083>: `/help`.\nOther: `/jishaku` (External Extension).", inline=False)
        e.add_field(name="Versions", value=f"Earth: v1.2.2\nPython: {platform.python_version()}\ndiscord.py: v{discord.__version__}", inline=False)
        e.add_field(name="Credits", value="**Hosting:** [Library of Code](https://loc.sh/discord)\n**Inspiration for `/kill`, `/gaypercent` and `/8ball`:** [Dank Memer](https://dankmemer.lol) bot.\n**Inspiration for `/uwu`:** [Reddit UwUtranslator bot](https://reddit.com/u/uwutranslator)\n**Cats:** [TheCatAPI](https://thecatapi.com)\n**Dogs:** [TheDogAPI](https://thedogapi.com)\n**Foxes:** [Random Fox](https://randomfox.ca)", inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="invite", description="Invite Earth to your server!")
    async def _invite(self, ctx: slash.SlashContext):
        await ctx.send("**Coming soon...**")
    
    @slashcog.cog_slash(name="support", description="Join the Planet Earth server for support with the bot.")
    async def _support(self, ctx: slash.SlashContext):
        await ctx.send("https://discord.gg/DsARcGwwdM")
    
    @slashcog.cog_slash(name="guilds", description="You found a Developer command!\nThere's a good chance you can't use this.", guild_ids=[832594030264975420], default_permission=False, options=[
        slash.utils.manage_commands.create_option("datatype", "Data to find.", 3, True, choices=[
            slash.utils.manage_commands.create_choice("all", "all"),
            slash.utils.manage_commands.create_choice("name", "name"),
            slash.utils.manage_commands.create_choice("id", "ID"),
            slash.utils.manage_commands.create_choice("owner", "owner"),
            slash.utils.manage_commands.create_choice("invite", "invite")
        ])
    ])
    @commands.is_owner()
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
        
        e = discord.Embed(title=f"Guilds [type=\"{typex}\"]", color=0x00a8ff, description=data)
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="restart", description="You found a Developer command!\nThere's a good chance you can't use this.", guild_ids=[832594030264975420], default_permission=False)
    @commands.is_owner()
    async def _restart(self, ctx: slash.SlashContext):
        restarting = await ctx.send(self.loading("Restarting..."))

        await self.bot.logout()
        await self.bot.login(self.token)

        await restarting.edit(content="<:Yes:833293078197829642> **Successfully restarted!**")
    
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
        slashbug = await ctx.send("Successfully executed command!")
        await asyncio.sleep(1.0)
        await slashbug.delete()
    
    @slashcog.cog_slash(name="uwu", description="Reject English, evolve to Furry.", options=[
        slash.utils.manage_commands.create_option("sentence", "This is what will be turned into the UwU language.", 3, True)
    ])
    async def _uwu(self, ctx: slash.SlashContext, sentence):
        await ctx.send(self.uwufy(sentence))
    
    @slashcog.cog_slash(name="cat", description="Shows a random image of a cat.")
    async def _cat(self, ctx: slash.SlashContext):
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
    
    @slashcog.cog_slash(name="dog", description="Shows a random image of a dog.")
    async def _dog(self, ctx: slash.SlashContext):
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
    
    @slashcog.cog_slash(name="fox", description="Shows a random image of a fox.")
    async def _fox(self, ctx: slash.SlashContext):
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
    
    @slashcog.cog_slash(name="hug", description="Hugs the user you want.", options=[
        slash.utils.manage_commands.create_option("member", "The user you want to hug. You can select from the popup list, type their username, or their ID.", 6, True),
        slash.utils.manage_commands.create_option("message", "Something you'd like to tell who you just hugged, for example why you decided to do so.", 3, False)
    ])
    async def _hug(self, ctx: slash.SlashContext, member, message=None):
        huglineint = random.randint(0, 9)
        halfpoint = self.huglines[str(huglineint)].replace("author", ctx.author.mention)
        hugline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Hug", color=0x00a8ff, description=f"{hugline}")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        if message is not None:
            e.add_field(name=f"{ctx.author.name} included a message! They said...", value=f"{message}", inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="kill", description="Kills the user you want.", options=[
        slash.utils.manage_commands.create_option("member", "The user you want to kill. You can select from the popup list, type their username, or their ID.", 6, True)
    ])
    async def _kill(self, ctx: slash.SlashContext, member):
        killlineint = random.randint(0, 4)
        halfpoint = self.killlines[str(killlineint)].replace("author", ctx.author.mention)
        killline = halfpoint.replace("member", member.mention)
        
        e = discord.Embed(title="Murder", color=0x00a8ff, description=f"{killline}")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
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
    
    @slashcog.cog_slash(name="8ball", description="Seek an answer from the Magic 8 Ball.", options=[
        slash.utils.manage_commands.create_option("question", "What you want to ask the Magic 8 Ball.", 3, True)
    ])
    async def _eightball(self, ctx: slash.SlashContext, question):
        balllineint = random.randint(0, 4)
        ballline = self.balllines[str(balllineint)]

        e = discord.Embed(title="Magic 8 Ball", color=0x00a8ff)
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Your Question", value=f"{question}", inline=False)
        e.add_field(name="The 8 Ball's Answer", value=f"{ballline}", inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="poll", description="Create a poll. Currently only supports two options.", options=[
        slash.utils.manage_commands.create_option("name", "The poll's name.", 3, True),
        slash.utils.manage_commands.create_option("option1", "The first option to vote on.", 3, True),
        slash.utils.manage_commands.create_option("option2", "The second option to vote on.", 3, True)
    ])
    async def _poll(self, ctx: slash.SlashContext, name: str, option1: str, option2: str):
        vote1 = 0
        vote2 = 0

        e = discord.Embed(title=f"Poll: {name}", color=0x00a8ff, description=f"**Poll by {ctx.author.mention}.**\nThink and choose. You cannot change your answer.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Votes", value=f"`{option1} (1)`: {vote1}\n`{option2} (2)`: {vote2}", inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        poll = await ctx.send(embed=e, components=[
            slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "1st Option"),
            slash.utils.manage_components.create_button(slash.utils.manage_components.ButtonStyle.blue, "2nd Option")
        ])

        waitfor1 = await self.bot.wait_for("button_click", check=lambda r: r.component.label.startswith("1st"))
        if waitfor1.channel == ctx.channel:
            vote1 += 1
            await poll.edit(content=None, embed=e)
        waitfor2 = await self.bot.wait_for("button_click", check=lambda r: r.component.label.startswith("2nd"))
        if waitfor2.channel == ctx.channel:
            vote2 += 1
            await poll.edit(content=None, embed=e)
    
    @slashcog.cog_slash(name="uptime", description="Shows an Embed with Earth's uptime.")
    async def _uptime(self, ctx: slash.SlashContext):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        e = discord.Embed(title="Uptime", color=0x00a8ff, description=f"The bot has been online for:\n{days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Last Restart", value="The bot was last restarted on {} UTC".format(self.bot.launch_time.strftime("%A, %d %B %Y at %H:%M")), inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="ping", description="Shows an Embed with Earth's ping latency.")
    async def _ping(self, ctx: slash.SlashContext):
        ping = self.bot.latency * 1000
        pingr = round(ping, 1)
        e = discord.Embed(title="Ping Latency", color=0x00a8ff, description=f"My ping latency is {pingr}ms. It's the time it takes for my host's servers to reach Discord.")
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="userinfo", description="Retrieves information about a user.", options=[
        slash.utils.manage_commands.create_option("user", "The user to find.", 3, False)
    ])
    async def _userinfo(self, ctx: slash.SlashContext, user=None):
        if user is None:
            fetching = await ctx.send(self.loading("Retrieving data for the requested User. Please wait."))

            string = ""
            for role in ctx.author.roles:
                if role == ctx.guild.default_role:
                    continue
                string = string + f"{role.mention} "

            e = discord.Embed(title=f"Information for {str(ctx.author)}", color=0x00a8ff)
            e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
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
            e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
            await fetching.edit(content=None, embed=e)
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

                fetching = await ctx.send(self.loading("Retrieving data for the requested User. Please wait."))

                string = ""
                for role in user.roles:
                    if role == ctx.guild.default_role:
                        continue
                    string = string + f"{role.mention} "

                e = discord.Embed(title=f"Information for {str(user)}", color=0x00a8ff)
                e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
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
                e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
                await fetching.edit(content=None, embed=e)
            else:
                user = await self.bot.fetch_user(user)

                if user in ctx.guild.members:
                    user = ctx.guild.get_member(user.id)

                    fetching = await ctx.send(self.loading("Retrieving data for the requested User. Please wait."))

                    string = ""
                    for role in user.roles:
                        if role == ctx.guild.default_role:
                            continue
                        string = string + f"{role.mention} "

                    e = discord.Embed(title=f"Information for {str(user)}", color=0x00a8ff)
                    e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
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
                    e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
                    await fetching.edit(content=None, embed=e)
                else:
                    fetching = await ctx.send("<a:aEarthLoading:734878543967813652> **Retrieving data for the requested User. Please wait.**")

                    e = discord.Embed(title=f"Information for {str(user)}", color=0x00a8ff)
                    e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
                    e.set_thumbnail(url=user.avatar_url)
                    e.add_field(name="Username", value=f"{user.name}")
                    e.add_field(name="Discriminator", value=f"{user.discriminator}")
                    e.add_field(name="ID", value=f"{user.id}")
                    e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")))
                    e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
                    await fetching.edit(content=None, embed=e)
    
    @slashcog.cog_slash(name="serverinfo", description="Shows information about the Context Guild.")
    async def serverinfo(self, ctx: slash.SlashContext):
        fetching = await ctx.send(self.loading("Retrieving data for this Guild. Please wait."))
            
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
            
        e = discord.Embed(title=f"Information for {ctx.guild.name}", color=0x00a8ff)
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
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
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await fetching.edit(content=None, embed=e)
    
    @slashcog.cog_slash(name="nitro", description="Sends animated emojis (from this server) with your name.", options=[
        slash.utils.manage_commands.create_option("emojiname", "The emoji (from this server) that you want to use's name.", 3, True)
    ])
    async def _nitro(self, ctx: slash.SlashContext, emojiname):
        emoji = discord.utils.get(ctx.guild.emojis, name=emojiname)

        avatar = await ctx.author.avatar_url.read()
        webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=avatar, reason="Nitro command.")

        await webhook.send(f"<a:{emoji.name}:{emoji.id}>")
        await ctx.message.delete()
        await webhook.delete()

def setup(bot: commands.Bot):
    bot.add_cog(Slash(bot))
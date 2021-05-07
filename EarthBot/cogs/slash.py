import discord
import discord_slash as slash
import random
import asyncio
import aiohttp
from datetime import datetime
from discord_slash import cog_ext as slashcog
from discord.ext import commands

class Slash(commands.Cog):
    """Slash commands."""

    def __init__(self, bot):
        self.bot = bot
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> {sentence}"
    
    def uwufy(self, sentence: str):
        uwu = sentence.lower()
        uwu = uwu.replace("l", "w")
        uwu = uwu.replace("r", "w")
        uwu = uwu.replace("th", "d")
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
        e.add_field(name="Developers", value="<@450678229192278036>: `e.info`, AutoPublish, AutoPing, `e.say`, `e.cat`, `e.dog`, `e.fox`, `e.ping`, `e.uptime`, `e.userinfo`, `e.serverinfo`, `e.nitro`.\n<@598325949808771083>: `e.help`.\nOther: `e.uwu` (Inspired by <@788483848127905844>'s old code, coded by <@450678229192278036>), `e.jishaku` (External Extension).", inline=False)
        if luckyint == 69:
            e.set_field_at(0, name="Developers", value="<@450678229192278036>: `e.info`, AutoPublish, AutoPing, `e.arth`, `e.say`, `e.cat`, `e.dog`, `e.fox`, `e.ping`, `e.uptime`, `e.userinfo`, `e.serverinfo`, `e.nitro`.\n<@598325949808771083>: `e.help`.\nOther: `e.uwu` (Inspired by <@788483848127905844>'s old code, coded by <@450678229192278036>), `e.jishaku` (External Extension).", inline=False)
        e.add_field(name="Versions", value=f"Earth: v1.1.2\ndiscord.py: v{discord.__version__}", inline=False)
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @slashcog.cog_slash(name="arth", description="???")
    async def _arth(self, ctx: slash.SlashContext):
        await ctx.send("hello there")

        def check(m):
            return m.content.lower() == "general kenobi" and m.channel == ctx.channel
        
        try:
            waitfor = await self.bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            return
        else:
            await ctx.send(f"Huzzah! A man of quality! Nice one, {waitfor.author.name}!")
    
    @slashcog.cog_slash(name="say", description="The bot will say what you tell it to.", options=[
        slash.utils.manage_commands.create_option("message", "Whatever you type after this option will be what is going to be said.", 3, False), 
        slash.utils.manage_commands.create_option("anonymous", "Include this to make your message anonymous.", 5, False),
        slash.utils.manage_commands.create_option("uwu", "Include this to turn your message to UwU.", 5, False),
        slash.utils.manage_commands.create_option("channel", "Include this to send your message in a channel that isn't the Context channel.", 7, False),
        slash.utils.manage_commands.create_option("user", "Include this to send the message as another user.", 6, False)
        ])
    async def _say(self, ctx: slash.SlashContext, message="https://discord.gg/GFkEMD45xg", anonymous=False, uwu=False, channel=None, user=None):
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
    
    @slashcog.cog_slash(name="userinfo", description="Retrieves information about a user. Thanks to API calls, it works even if the person you search for is outside the server!", options=[
        slash.utils.manage_commands.create_option("user", "The user to find. You can select from the popup list, use @mention, username, username#discriminator, or an ID.", 6, False)
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

def setup(bot):
    bot.add_cog(Slash(bot))
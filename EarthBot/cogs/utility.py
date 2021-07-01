import discord
import json
from datetime import datetime
from discord.ext import commands

class RolesView(discord.ui.View):
    """`e.roles`'s View."""

    def __init__(self):
        super().__init__()
        self.add_item(RolesSelect())
    
    async def process_inputs(self, select: discord.ui.Select, interaction: discord.Interaction):
        for selected in select.values:
            role = interaction.guild.get_role(int(selected))
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role, reason="Roles command.")
                await interaction.response.send_message(f"{role.name} Role removed successfully.", ephemeral=True)
            else:
                await interaction.user.add_roles(role, reason="Roles command.")
                await interaction.response.send_message(f"{role.name} Role added successfully.", ephemeral=True)

class RolesSelect(discord.ui.Select):
    """`e.roles`'s Select."""

    view: RolesView

    def __init__(self):
        super().__init__(placeholder="Select 1 or more Role(s).", max_values=25, options=[
            discord.SelectOption(label="Planet Earth", value="858825115672379423", description="News, Events, and Fundraisers"),
            discord.SelectOption(label="Earth Development", value="858825487522463784", description="Earth Bot Updates and Coding Help"),
            discord.SelectOption(label="Earth Games", value="858825447059882014", description="Soon...")
        ])
    
    async def callback(self, interaction: discord.Interaction):
        await self.view.process_inputs(self, interaction)

class Utility(commands.Cog):
    """The cog for Earth's utilities."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./Earth/EarthBot/misc/assets/embed.json") as embeds:
            self.embed = json.load(embeds)
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> **{sentence}**"

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.launch_time = datetime.utcnow()
    
    @commands.command(name="uptime", aliases=["up", "upt"])
    async def uptime(self, ctx: commands.Context):
        """Shows an Embed with Earth's uptime."""

        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        e = discord.Embed(title="Uptime", color=int(self.embed["color"], 16), description=f"The bot has been online for:\n{days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")
        e.set_author(name=self.embed["authorname"], icon_url="https://this.is-for.me/i/gxe1.png")
        e.add_field(name="Last Restart", value="The bot was last restarted on {} UTC".format(self.bot.launch_time.strftime("%A, %d %B %Y at %H:%M")), inline=False)
        e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.message.reply(embed=e)
    
    @commands.command(name="ping", aliases=["latency", "lat"])
    async def ping(self, ctx: commands.Context):
        """Shows an Embed with Earth's ping latency."""

        ping = self.bot.latency * 1000
        pingr = round(ping, 1)
        e = discord.Embed(title="Ping Latency", color=int(self.embed["color"], 16), description=f"My ping latency is {pingr}ms. It's the time it takes for my host's servers to reach Discord.")
        e.set_author(name=self.embed["authorname"], icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.message.reply(embed=e)
    
    @commands.command(name="userinfo", aliases=["ui", "memberinfo", "mi"])
    async def userinfo(self, ctx: commands.Context, user=None):
        """Retrieves information about a user. Thanks to API calls, it works even if the person you search for is outside the server!"""

        if user is None:
            await ctx.trigger_typing()

            string = ""
            for role in ctx.author.roles:
                if role == ctx.guild.default_role:
                    continue
                string = string + f"{role.mention} "

            e = discord.Embed(title=f"Information for {str(ctx.author)}", color=int(self.embed["color"], 16))
            e.set_author(name=self.embed["authorname"], icon_url="https://this.is-for.me/i/gxe1.png")
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
            e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
            await ctx.message.reply(embed=e)
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

                await ctx.trigger_typing()

                string = ""
                for role in user.roles:
                    if role == ctx.guild.default_role:
                        continue
                    string = string + f"{role.mention} "

                e = discord.Embed(title=f"Information for {str(user)}", color=int(self.embed["color"], 16))
                e.set_author(name=self.embed["authorname"], icon_url="https://this.is-for.me/i/gxe1.png")
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
                e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
                await ctx.message.reply(embed=e)
            else:
                user = await self.bot.fetch_user(user)

                if user in ctx.guild.members:
                    user = ctx.guild.get_member(user.id)

                    await ctx.trigger_typing()

                    string = ""
                    for role in user.roles:
                        if role == ctx.guild.default_role:
                            continue
                        string = string + f"{role.mention} "

                    e = discord.Embed(title=f"Information for {str(user)}", color=int(self.embed["color"], 16))
                    e.set_author(name=self.embed["authorname"], icon_url="https://this.is-for.me/i/gxe1.png")
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
                    e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
                    await ctx.message.reply(embed=e)
                else:
                    await ctx.trigger_typing()

                    e = discord.Embed(title=f"Information for {str(user)}", color=int(self.embed["color"], 16))
                    e.set_author(name=self.embed["authorname"], icon_url="https://this.is-for.me/i/gxe1.png")
                    e.set_thumbnail(url=user.avatar_url)
                    e.add_field(name="Username", value=f"{user.name}")
                    e.add_field(name="Discriminator", value=f"{user.discriminator}")
                    e.add_field(name="ID", value=f"{user.id}")
                    e.add_field(name="Created At", value="{} UTC".format(user.created_at.strftime("%A, %d %B %Y at %H:%M")))
                    e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
                    await ctx.message.reply(embed=e)
    
    @commands.command(name="serverinfo", aliases=["si", "guildinfo", "gi"])
    async def serverinfo(self, ctx: commands.Context):
        """Shows information about the Context Guild."""

        await ctx.trigger_typing()
            
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
        e.set_author(name=self.embed["authorname"], icon_url="https://this.is-for.me/i/gxe1.png")
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
        e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.message.reply(embed=e)
    
    @commands.command(name="emojiinfo")
    async def emojiinfo(self, ctx: commands.Context, emoji):
        """Shows information about an Emoji in this server."""

        await ctx.message.reply("<:No:833293106198872094> This command is broken at the moment.")

#        emoji = discord.utils.get(ctx.guild.emojis, name=emoji)

#        e = discord.Embed(title=f"Information about {emoji.name}", color=int(self.embed["color"], 16))
#        e.set_author(name=self.embed["authorname"], icon_url="https://this.is-for.me/i/gxe1.png")
#        e.set_thumbnail(url=emoji.url)
#        e.add_field(name="Name", value=f"{emoji.name}")
#        e.add_field(name="ID", value=f"{emoji.id}")
#        e.add_field(name="Animated", value=f"{emoji.animated}")
#        e.add_field(name="Created At", value="{} UTC".format(emoji.created_at.strftime("%A, %d %B %Y at %H:%M")))
#        e.set_footer(text=self.embed["footer"], icon_url="https://this.is-for.me/i/gxe1.png")
#        await ctx.message.reply(embed=e, components=[
#            [
#                components.Button(label="Use Emoji", style=components.ButtonStyle.blue, id="use", emoji=emoji)
#            ]
#        ])

#        waitfor = await self.bot.wait_for("button_click", check=lambda r: r.component.id == "use")
#        if waitfor.user.id == ctx.author.id:
#            componentbug = await waitfor.respond("Emoji used successfully!")
#            await self.nitro(ctx, emoji.name)
#            await asyncio.sleep(1.0)
#            await componentbug.delete()
    
    @commands.command(name="discord")
    async def discord(self, ctx: commands.Context):
        """As a normal command could create confusion, this command is only available in Slash. Use `/discord <subcommand>`."""

        await ctx.message.reply("As a normal command could create confusion, this command is only available in Slash. Use `/discord <subcommand>`.")
    
    @commands.command(name="nitro")
    async def nitro(self, ctx: commands.Context, emoji):
        """Sends animated emojis (from this server) with your name."""

        await ctx.message.reply("<:No:833293106198872094> This command is broken at the moment.")

#        emoji = discord.utils.get(ctx.guild.emojis, name=emoji)

#        avatar = await ctx.author.avatar_url.read()
#        webhook = await ctx.channel.create_webhook(name=ctx.author.name, avatar=avatar, reason="Nitro command.")

#        await webhook.send(f"<a:{emoji.name}:{emoji.id}>")
#        await ctx.message.delete()
#        await webhook.delete()

    @commands.command(name="roles")
    async def roles(self, ctx: commands.Context):
        """Add/remove Roles to/from yourself via a Select."""

        e = discord.Embed(title="Add/Remove Roles", color=int(self.embed["color"], 16), description="Select the Roles to add/remove to/from yourself.")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.message.reply(embed=e, view=RolesView())

def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))

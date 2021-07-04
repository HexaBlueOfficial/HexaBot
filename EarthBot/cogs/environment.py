import discord
import json
from discord.ext import commands

class GetUpdatesFlags(commands.FlagConverter):
    updates: str = commands.flag(aliases=["from"], max_args=1)
    to: discord.TextChannel

class UnrecognisedUpdates(Exception):
    def __init__(self):
        super().__init__("Updates type was not recognised")

class Environment(commands.Cog):
    """Commands for the Environment!"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./Earth/EarthBot/misc/assets/embed.json") as embeds:
            self.embed = json.load(embeds)

    @commands.command(name="getupdates")
    @commands.has_permissions(manage_channels=True)
    async def getupdates(self, ctx: commands.Context, flags: GetUpdatesFlags):
        """Get updates about the Earth.\n\nFlags:\n`updates:`/`from:` - The Updates to get. (`globalwarming`, `endangeredspecies`, `evilcompanies`)\n`to:` - The channel where to get them.\n\nExample command:\n`e.getupdates updates: globalwarming to: #mycoolchannel`"""

        updates = flags.updates
        to = flags.to

        if updates == "globalwarming":
            updates = 832660792397791262
        elif updates == "endangeredspecies":
            updates = 832661047398760450
        elif updates == "evilcompanies":
            updates = 832671013753454602
        else:
            raise UnrecognisedUpdates
        
        earthnet = self.bot.get_guild(832594030264975420)
        channel = earthnet.get_channel(updates)

        await channel.follow(destination=to, reason="GetUpdates command.")
        
        followed = ""
        if updates == 832660792397791262:
            followed = "Global Warming Updates"
        elif updates == 832661047398760450:
            followed = "Endangered Species Updates"
        elif updates == 832671013753454602:
            followed = "Evil Companies Updates"
        await ctx.message.reply(f"Successfully followed {followed}.")
    
    @commands.command(name="fundraiser")
    async def fundraiser(self, ctx: commands.Context):
        """This command gets updated everytime a new Fundraiser starts in the EarthNetwork server."""

        e = discord.Embed(title="How to donate to WWF", color=int(self.embed["color"], 16), description="**How to donate to WWF:**\n\n**Step 1:** Go to https://worldwildlife.org (WWF's official website).\n**Step 2:** Hover over the big, red, \"DONATE\" button.\n**Step 3:** Select \"Make a One-time Donation\" from the dropdown.\n**Step 4:** Select what you prefer and enter your info.\n**Step 5:** Press \"Submit\".\n\nCongratulations: you helped our Planet!")
        e.set_author(name="{}".format(self.embed["authorname"] + "Environment"), icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.message.reply(embed=e)

def setup(bot):
    bot.add_cog(Environment(bot))
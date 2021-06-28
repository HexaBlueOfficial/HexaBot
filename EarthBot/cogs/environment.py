import discord
import json
from discord.ext import commands

class Environment(commands.Cog):
    """Commands for the Environment!"""

    def __init__(self, bot):
        self.bot = bot
        with open("./Earth/EarthBot/misc/assets/embed.json") as embeds:
            self.embed = json.load(embeds)

    @commands.command(name="getupdates")
    async def getupdates(self, ctx: commands.Context):
        """As a normal command could create confusion, this command is only available in Slash. Use `/getupdates`."""

        await ctx.send("As a normal command could create confusion, this command is only available in Slash. Use `/getupdates`.")
    
    @commands.command(name="fundraiser")
    async def fundraiser(self, ctx: commands.Context):
        """This command gets updated everytime a new Fundraiser starts in the EarthNetwork server."""

        e = discord.Embed(title="How to donate to WWF", color=int(self.embed["color"], 16), description="**How to donate to WWF:**\n\n**Step 1:** Go to https://worldwildlife.org (WWF's official website).\n**Step 2:** Hover over the big, red, \"DONATE\" button.\n**Step 3:** Select \"Make a One-time Donation\" from the dropdown.\n**Step 4:** Select what you prefer and enter your info.\n**Step 5:** Press \"Submit\".\n\nCongratulations: you helped our Planet!")
        e.set_author(name=self.embed["authorname"], icon_url=self.embed["icon"])
        e.set_footer(text=self.embed["footer"], icon_url=self.embed["icon"])
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Environment(bot))
import discord
import json
from discord.ext import commands, flags

class TypeNotRecognised(Exception):
    pass

class Developer(commands.Cog):
    """Developer stuff."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./Earth/EarthBot/misc/assets/embed.json") as embeds:
            self.embed = json.load(embeds)
        with open("./token.json") as tokenfile:
            tokendict = json.load(tokenfile)
        self.token = tokendict["token"]
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> **{sentence}**"
    
    @flags.add_flag("--type", type=str, default="all")
    @flags.command(name="guilds", hidden=True)
    @commands.is_owner()
    async def guilds(self, ctx: commands.Context, **flags):
        """You found a Developer command!\nYou can't use this command, so why seek help for it?"""
        
        typex = flags["type"]
        
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
    
    @commands.command(name="restart", hidden=True)
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        """You found a Developer command!\nYou can't use this command, so why seek help for it?"""

        await ctx.send(self.loading("Restarting... See you in a bit!"))

        await self.bot.close()
        await self.bot.login(self.token)

def setup(bot: commands.Bot):
    bot.add_cog(Developer(bot))
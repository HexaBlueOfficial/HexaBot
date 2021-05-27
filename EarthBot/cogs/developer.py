import discord
import json
from discord.ext import commands, flags

class TypeNotRecognised(Exception):
    pass

class Developer(commands.Cog):
    """Developer stuff."""

    def __init__(self, bot):
        self.bot = bot
        with open("./token.json") as tokenfile:
            tokendict = json.load(tokenfile)
        self.token = tokendict["token"]
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> **{sentence}**"
    
    @flags.add_flag("--type", type=str, default="all")
    @flags.command(name="guilds", hidden=True)
    @commands.is_owner()
    async def guilds(self, ctx, **flags):
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
        
        e = discord.Embed(title=f"Guilds [type=\"{typex}\"]", color=0x00a8ff, description=data)
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)
    
    @commands.command(name="restart")
    @commands.is_owner()
    async def restart(self, ctx):
        """You found a Developer command!\nYou can't use this command, so why seek help for it?"""

        restarting = await ctx.send(self.loading("Restarting..."))

        await self.bot.logout()
        await self.bot.login(self.token)

        await restarting.edit(content="<:Yes:833293078197829642> **Successfully restarted!**")

def setup(bot):
    bot.add_cog(Developer(bot))
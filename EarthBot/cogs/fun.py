import discord
from discord.ext import commands, flags

class Fun(commands.Cog):
    """The cog for Earth's fun commands."""

    def __init__(self, bot):
        self.bot = bot
    
    @flags.add_flag("-m", default="")
    @flags.add_flag("-a", action="store_true")
    @flags.add_flag("-u", type=discord.User, default=None)
    @flags.add_flag("-c", type=discord.TextChannel, default=None)
    @flags.command(name="say")
    async def say(self, ctx, **flags):
        """The bot will say what you tell him to.\n\nFlags:\n`-m` - Message flag. Whatever you put after this flag and before the next flag will be the message repeated by the bot. If your message has more than a word, use quotation marks.\n`-a` - Anonymization flag. Makes your message (`-m` flag content) anonymous.\n`-u` - User flag. Makes it look like another user sent your message (`-m` flag content). Works with username, username#discriminator, @mention and ID. Users outside this server will not work.\n`-c` - Channel flag. Sends the message in the channel you specify"""

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

        await webhook.send(flags["m"])
        await ctx.message.delete()
        await webhook.delete()
    
    @commands.command(name="uwu")
    async def uwu(self, ctx, sentence: str):
        """Reject English, evolve to Furry."""

        uwu = sentence.lower()
        uwu = uwu.replace("l", "w")
        uwu = uwu.replace("r", "w")
        uwu = uwu.replace("th", "d")
        await ctx.send(f"{uwu}, uwu *rawr* XD!")

def setup(bot):
    bot.add_cog(Fun(bot))
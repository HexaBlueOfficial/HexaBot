import discord
import asyncpg
from datetime import datetime
from discord.ext import commands

class Economy(commands.Cog):
    """The cog for Earth's EarthCoins economy."""

    def __init__(self, bot):
        self.bot = bot
    
    async def pgexecute(self, sql):
        db = await asyncpg.connect("postgres://tkhpexvxkfisim:14897b63a93fc0792007cc08660e4d451a0cf466c5c2490d8a2fae650da4dedf@ec2-23-23-128-222.compute-1.amazonaws.com:5432/d83ilreftm12s3")
        await db.execute(f'''{sql}''')
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> **{sentence}**"
    
    @commands.group(name="coins", aliases=["earths", "earthcoins", "economy", "ec"], invoke_without_command=True)
    async def coins(self, ctx):
        """Base command. Runs `e.coins profile` if without subcommands."""

        await self.profile(ctx)
    
    @coins.group(name="profile", invoke_without_command=True)
    async def profile(self, ctx, user=None):
        """Views your profile, or another's."""

        if user is None:
            try:
                creationdate = await self.pgexecute(f"SELECT cdate FROM economy WHERE cdate = '{ctx.author.id}\n%'").strftime("%A, %d %B %Y at %H:%M")
            except asyncpg.exceptions.NoDataFoundError:
                await ctx.send("<:No:833293106198872094> It doesn't look like you have a profile. Create one with `e.coins profile create`.")
            else:
                e = discord.Embed(name=f"{str(ctx.author)}'s EarthCoins Profile", color=0x00a8ff)
                e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
                e.add_field(name="Name", value=f"{ctx.author.name}")
                e.add_field(name="Discriminator", value=f"{ctx.author.discriminator}")
                e.add_field(name="Balance", value="Run `e.balance`.")
                e.add_field(name="Creation Date", value=f"{creationdate} UTC")
                e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
                await ctx.send(embed=e)
        else:
            try:
                user = int(user)
            except:
                user = str(user).lstrip("<@!")
                user = user.rstrip(">")
                user = int(user)

                user = self.bot.get_user(user)

                try:
                    creationdateq = await self.pgexecute(f"SELECT cdate FROM economy WHERE cdate = '{user.id}\n%'").splitlines()
                    creationdate = creationdateq[1].strftime("%A, %d %B %Y at %H:%M")
                    wins = await self.pgexecute(f"SELECT wins FROM economy WHERE wins = '{ctx.author.id}\n%'").splitlines()
                    losses = await self.pgexecute(f"SELECT losses FROM economy WHERE losses = '{ctx.author.id}\n%'").splitlines()
                    wallet = await self.pgexecute(f"SELECT wallet FROM economy WHERE wallet = '{ctx.author.id}\n%'").splitlines()
                    bank = await self.pgexecute(f"SELECT bank FROM economy WHERE bank = '{ctx.author.id}\n%'").splitlines()
                except asyncpg.exceptions.NoDataFoundError:
                    await ctx.send("<:No:833293106198872094> It doesn't look like you have a profile. Create one with `e.coins profile create`.")
                else:
                    e = discord.Embed(name=f"{str(user)}'s EarthCoins Profile", color=0x00a8ff)
                    e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
                    e.add_field(name="Name", value=f"{user.name}")
                    e.add_field(name="Discriminator", value=f"{user.discriminator}")
                    e.add_field(name="Balance", value=f"Wallet: {wallet[1]}\nBank: {bank[1]}")
                    e.add_field(name="Scenarios", value=f"Good: {wins[1]}\nBad: {losses[1]}")
                    e.add_field(name="Luck", value=f"{int(wins[1]) - int(losses[1])}")
                    e.add_field(name="Creation Date", value=f"{creationdate} UTC")
                    e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
                    await ctx.send(embed=e)
            else:
                user = await self.bot.fetch_user(user)

                try:
                    creationdateq = await self.pgexecute(f"SELECT cdate FROM economy WHERE cdate = '{user.id}\n%'").splitlines()
                    creationdate = creationdateq[1].strftime("%A, %d %B %Y at %H:%M")
                    wins = await self.pgexecute(f"SELECT wins FROM economy WHERE wins = '{ctx.author.id}\n%'").splitlines()
                    losses = await self.pgexecute(f"SELECT losses FROM economy WHERE losses = '{ctx.author.id}\n%'").splitlines()
                    wallet = await self.pgexecute(f"SELECT wallet FROM economy WHERE wallet = '{ctx.author.id}\n%'").splitlines()
                    bank = await self.pgexecute(f"SELECT bank FROM economy WHERE bank = '{ctx.author.id}\n%'").splitlines()
                except asyncpg.exceptions.NoDataFoundError:
                    await ctx.send("<:No:833293106198872094> It doesn't look like you have a profile. Create one with `e.profile create`.")
                else:
                    e = discord.Embed(name=f"{str(user)}'s EarthCoins Profile", color=0x00a8ff)
                    e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
                    e.add_field(name="Name", value=f"{user.name}")
                    e.add_field(name="Discriminator", value=f"{user.discriminator}")
                    e.add_field(name="Balance", value=f"Wallet: {wallet[1]}\nBank: {bank[1]}")
                    e.add_field(name="Scenarios", value=f"Good: {wins[1]}\nBad: {losses[1]}")
                    e.add_field(name="Luck", value=f"{int(wins[1]) - int(losses[1])}")
                    e.add_field(name="Creation Date", value=f"{creationdate} UTC")
                    e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
                    await ctx.send(embed=e)
    
    @profile.command(name="create")
    async def create(self, ctx):
        """Creates your EarthCoins profile."""

        creating = await ctx.send(self.loading("Creating your EarthCoins profile..."))

        try:
            await self.pgexecute(f"SELECT cdate FROM economy WHERE cdate = '{ctx.author.id}\n%'")
        except asyncpg.exceptions.NoDataFoundError:
            await self.pgexecute(f"INSERT INTO economy(wallet) VALUES ('{ctx.author.id}\n0')")
            await self.pgexecute(f"INSERT INTO economy(bank) VALUES ('{ctx.author.id}\n0')")
            await self.pgexecute(f"INSERT INTO economy(wins) VALUES ('{ctx.author.id}\n0')")
            await self.pgexecute(f"INSERT INTO economy(losses) VALUES ('{ctx.author.id}\n0')")
            await self.pgexecute(f"INSERT INTO economy(cdate) VALUES ('{ctx.author.id}\n{datetime.utcnow()}')")

            e = discord.Embed(title="EarthCoins Profile Creation Successful", color=0x00a8ff, description="Your EarthCoins Profile has been successfully created! Get playing!")
            e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
            e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
            await creating.edit(content=None, embed=e)
        else:
            await creating.edit(content="<:No:833293106198872094> You already have an EarthCoins profile. If you were looking for a user named \"create\", note that usernames won't work. Use the ID or mention them.")
    
    @commands.command(name="work")
    async def work(self, ctx):
        """Earn EarthCoins by legally working!"""

def setup(bot):
    bot.add_cog(Economy(bot))
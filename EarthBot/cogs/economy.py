import discord
import json
import asyncpg
import discord_slash as slash
import random
from datetime import datetime
from discord_slash import cog_ext as slashcog
from discord.ext import commands

class Economy(commands.Cog):
    """The cog for Earth's EarthCoins economy."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("./postgres.json") as postgresfile:
            postgresdict = json.load(postgresfile)
        self.postgres = postgresdict["creds"]
        with open("./Earth/EarthBot/misc/economy/work.json") as jobs:
            self.worklines = json.load(jobs)
    
    async def pgexecute(self, sql):
        db = await asyncpg.connect(self.postgres)
        await db.execute(f'''{sql}''')
    
    def loading(self, sentence):
        return f"<a:aLoading:833070225334206504> **{sentence}**"
    
    @slashcog.cog_slash(name="coins", description="Base command. Runs `e.coins profile` if without subcommands.")
    async def _coins(self, ctx: slash.SlashContext):
        await self.profile(ctx)
    
    @slashcog.cog_subcommand(base="coins", name="profile", description="Views your profile, or another's.", options=[
        slash.utils.manage_commands.create_option("user", "The user you want to see the profile of.", 3, False)
    ])
    async def _profile(self, ctx: slash.SlashContext, user=None):
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
    
    @slashcog.cog_subcommand(base="coins", subcommand_group="profile", name="create", description="Creates your EarthCoins profile.")
    async def _create(self, ctx: slash.SlashContext):
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
            await creating.edit(content="<:No:833293106198872094> You already have an EarthCoins profile.")
    
    @slashcog.cog_slash(name="work", description="Earn EarthCoins by legally working!")
    async def _work(self, ctx: slash.SlashContext):
        goodorbad = random.randint(0, 100)
        lineindex = str(random.randint(0, 9))
        
        mode = await self.pgexecute(f"SELECT mode FROM economy WHERE mode = '{ctx.guild.id}\n%'").splitlines()[1]
        if mode == "capi":
            modex = "Capitalism"
        elif mode == "comm":
            modex = "Communism"
        elif mode == "marx":
            modex = "Marxism"
        
        if goodorbad <= 75:
            if mode == "capi":
                earning = random.randint(50, 300)
                line = self.worklines["good"][lineindex].replace("earning", earning)
            elif mode == "comm":
                line = self.worklines["good"][lineindex].replace("earning", "50")
            elif mode == "marx":
                line = self.worklines["good"][lineindex].replace("earning", "300")
        else:
            if mode == "capi":
                loss = random.randint(10, 70)
                line = self.worklines["bad"][lineindex].replace("loss", loss)
            elif mode == "comm":
                line = self.worklines["bad"][lineindex].replace("loss", "70")
            elif mode == "marx":
                line = self.worklines["bad"][lineindex].replace("loss", "10")
        
        e = discord.Embed(title=f"Work ({modex} Mode)", color=0x00a8ff, description=line)
        e.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        e.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=e)

def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))
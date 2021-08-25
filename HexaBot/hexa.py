import discord
import json
import discord_slash as interactions
import tracemalloc
import typing
from discord.ext import commands

with open("./token.json") as tokenfile:
    token = json.load(tokenfile)
with open("./HexaBot/HexaBot/misc/assets/embed.json") as embedfile:
    embed = json.load(embedfile)

bot = commands.Bot(command_prefix=commands.when_mentioned_or("h."), intents=discord.Intents.all())
slash = interactions.SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

tracemalloc.start()

@bot.event
async def on_ready():
    channel = bot.get_channel(832677639944667186)
    await channel.send(f"**HexaBot** is ready and running on **discord.py v{discord.__version__}**!")

@bot.event
async def on_command_error(ctx: commands.Context, error):
    e = discord.Embed(title="An Error Occurred", color=int(embed["color"], 16), description=f"{error}")
    e.set_author(name=embed["author"] + "Main", icon_url=embed["icon"])
    e.set_footer(text=embed["footer"], icon_url=embed["icon"])
    await ctx.send(embed=e)

@bot.event
async def on_slash_command_error(ctx: typing.Union[interactions.SlashContext, interactions.MenuContext], ex):
    e = discord.Embed(title="An Error Occurred", color=int(embed["color"], 16), description=f"{ex}")
    e.set_author(name=embed["author"] + "Main", icon_url=embed["icon"])
    e.set_footer(text=embed["footer"], icon_url=embed["icon"])
    await ctx.send(embed=e)

extensions = ["cogs.core", "cogs.fun", "cogs.help", "cogs.utility"]
for extension in extensions:
    bot.load_extension(extension)

bot.run(token["hexa"])
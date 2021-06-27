import discord
import discord_slash as slasher
import tracemalloc
import discord_components as components
import json
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("e."), intents=discord.Intents.all())
slash = slasher.SlashCommand(bot, True, False, True, True)
bot.remove_command("help")

tracemalloc.start()

@bot.event
async def on_ready():
    components.DiscordComponents(bot)
    
    channel = bot.get_channel(832677639944667186)
    await channel.send(f"Python Earth is ready and running on discord.py v{discord.__version__}!")

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("<:No:833293106198872094> The command was not found. You may want to run `e.help` for a list of commands.")
    else:
        await ctx.send(f"<:No:833293106198872094> {error}")
    raise error

@bot.event
async def on_slash_command_error(ctx: slasher.SlashContext, ex):
    await ctx.send(f"<:No:833293106198872094> {ex}")
    raise ex

extensions = ["cogs.core", "cogs.developer", "cogs.environment", "cogs.fun", "cogs.help", "cogs.slash", "cogs.utility", "jishaku"]
for extension in extensions:
    bot.load_extension(extension)

with open("./token.json") as tokenfile:
    token = json.load(tokenfile)
bot.run(token["token"])
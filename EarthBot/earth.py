import discord
import tracemalloc
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("e."), intents=intents)
bot.remove_command("help")

tracemalloc.start()

@bot.event
async def on_ready():
    channel = bot.get_channel(832658141274439690)
    await channel.send(f"Earth is ready and running on discord.py v{discord.__version__}!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        handled = await ctx.send("<:No:833293106198872094> The command was not found. You may want to run `e.help` for a list of commands.")
    else:
        handled = await ctx.send(f"<:No:833293106198872094> {error}")
    await ctx.message.delete()
    await asyncio.sleep(5.0)
    await handled.delete()
    raise error

extensions = ["cogs.core", "cogs.fun", "cogs.help", "cogs.utility", "jishaku"]
for extension in extensions:
    bot.load_extension(extension)

bot.run("ODMzMDM4ODk5MzA2NjkyNjM5.YHsh7g.GSbwwFAfyiEXJLzSBSAclR6_2lo")
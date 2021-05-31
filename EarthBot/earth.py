import discord
import discord_slash as slasher
import discord_components as components
import tracemalloc
import asyncio
import json
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("e."), intents=discord.Intents.all())
slash = slasher.SlashCommand(bot, override_type=True, sync_commands=True, sync_on_cog_reload=True)
bot.remove_command("help")

tracemalloc.start()

@bot.event
async def on_ready():
    components.DiscordComponents(bot)

    channel = bot.get_channel(832677639944667186)
    await channel.send(f"Earth is ready and running on discord.py v{discord.__version__}!")

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        handled = await ctx.send("<:No:833293106198872094> The command was not found. You may want to run `e.help` for a list of commands.")
    else:
        handled = await ctx.send(f"<:No:833293106198872094> {error}")
    await ctx.message.delete()
    await asyncio.sleep(5.0)
    await handled.delete()
    raise error

extensions = ["cogs.core", "cogs.developer", "cogs.fun", "cogs.help", "cogs.slash", "cogs.utility", "jishaku"]
for extension in extensions:
    bot.load_extension(extension)

with open("./token.json") as tokenfile:
    tokendict = json.load(tokenfile)
token = tokendict["token"]
bot.run(token)
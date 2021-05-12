import discord
from discord.ext import commands

class HelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={'hidden': True})

    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

    def command_formatter(self, embed, command):
        embed.title = f"{self.get_command_signature(command)} (from {command.cog_name})"
        if command.description:
            embed.description = f'{command.description}\n\n{command.help}'
        else:
            embed.description = command.help or 'No help found'

    async def send_bot_help(self, mapping):
        ctx = self.context
        embed = discord.Embed(title="Earth's Commands", color=0x00a8ff, description="The following is a list of commands for Earth.")
        embed.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        embed.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        bot = self.context.bot
        filtered = await self.filter_commands(bot.commands, sort=True)
        for cog, cog_commands in mapping.items():
            filtered = await self.filter_commands(cog_commands)
            if filtered:
                embed.add_field(name=f"{cog.qualified_name}", value=cog.description or 'No description', inline=False)
                for command in filtered:
                    embed.add_field(name=f"`{self.get_command_signature(command)}`", value=f"{command.description}\n\n{command.short_doc}", inline=False)
        embed.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"{self.get_command_signature(command)} (from {command.cog_name})", description=command.help or 'No description', color=0x00a8ff)
        embed.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        embed.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        embed.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(color=0x00a8ff)
        embed.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        embed.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        embed.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        self.command_formatter(embed, group)

        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f"{cog.qualified_name}", description=cog.description or 'No description', color=0x00a8ff)
        embed.set_author(name="Earth", icon_url="https://this.is-for.me/i/gxe1.png")
        embed.set_thumbnail(url="https://this.is-for.me/i/gxe1.png")
        filtered = await self.filter_commands(cog.get_commands())
        if filtered:
            for command in filtered:
                self.add_command_field(embed, command)
        embed.set_footer(text="Earth by Earth Development", icon_url="https://this.is-for.me/i/gxe1.png")
        await self.context.send(embed=embed)

class Help(commands.Cog):
    """The cog for the bot's `help` command."""
    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.old_help_command

def setup(bot):
    bot.add_cog(Help(bot))
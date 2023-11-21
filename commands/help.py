from discord.ext import commands
from discord import app_commands
import importlib
import discord
import os


id = "1176163141953011802"
    
class Help(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        
    command_list = ""
    
    for cmd in os.listdir('commands'):
        if not cmd.startswith('_') and cmd[:-3] != 'help' and cmd.endswith('.py'):
            command = importlib.import_module(f'commands.{cmd[:-3]}')
            command_list += f"</{cmd[:-3]}:{int(command.id)}>\n"
    
    embed = discord.Embed(
        description=command_list
        )
    
    @commands.command()
    async def help(self, ctx: discord.Interaction) -> None:
        await ctx.send(embed=self.embed)
        
    @app_commands.command(name='help')
    async def _help(self, ctx) -> None:
        await ctx.response.send_message(embed=self.embed)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
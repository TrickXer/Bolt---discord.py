import discord
from discord.ext import commands
from discord import app_commands


id = "1044552464382308372"

class Ping(commands.Cog):    
    def __init__(self, client: commands.Bot):
        self.client = client

    # message command
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"> **Ping**: `{(round(self.client.latency * 1000, 2))} ms`")
        
    # slash command
    @app_commands.command(name='ping', description="shows bot's latency")
    async def _ping(self, ctx: discord.Interaction):
        await ctx.response.send_message(f"> **Ping**: `{round(self.client.latency * 1000, 2)} ms`")
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
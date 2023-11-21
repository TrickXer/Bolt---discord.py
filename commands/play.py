from functions.get_song import search
from discord.ext import commands
from discord import app_commands
import discord
import re


class InvalidQueryException(Exception):
    """Raised when the query is empty or None"""
    pass


id = "1044552464382308372"

class Play(commands.Cog):
    def __init__ (self, client: commands.Bot) -> None:
        self.client = client
        
    async def create_embed(self, ctx, query) -> discord.Embed:
        result = search(query=query)
    
        song_embed = discord.Embed(
            colour=discord.Colour.brand_red(),
            title=result['title'],
            description=re.sub(r'\W+', ' ', result['descriptionSnippet'][0]['text']),
            url=result['link']
        )
    
        song_embed.set_thumbnail(url=result['thumbnails'][0]['url'])
        
        song_embed.add_field(name='Channel', value=f"[{result['channel']['name']}]({result['channel']['link']})", inline=True)
        song_embed.add_field(name='Duration', value=f"`{result['duration']}`", inline=True)
        song_embed.add_field(name='Views', value=f"`{result['viewCount']['short']}`", inline=True)
        song_embed.add_field(name='Position in queue', value=f"`1`")
        
        song_embed.set_footer(text=f"\nRequesed by {ctx.message.author.display_name}", icon_url=ctx.message.author.display_avatar)
    
        return song_embed
    
    @commands.command()
    async def play(self, ctx):
        try:
            async with ctx.typing():
                query = ' '.join(re.sub('play', '', ctx.message.content).split(' ')[1:])
                
                if (query == ' ' or query == '' or query == None): 
                    raise InvalidQueryException
                else: 
                    song_embed = await self.create_embed(ctx=ctx, query=query)
                    await ctx.send(embed = song_embed)
        except InvalidQueryException:
            await ctx.send("> `play` command must contain an argument ❌")
    
    @app_commands.command(name='play', description="play's songs as per your request")
    async def _play(self, ctx: discord.Interaction):
        song_embed = await self.create_embed(ctx=ctx)
        await ctx.response.send_message(embed=song_embed)
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Play(bot))
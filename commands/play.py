from functions.get_song import YTDLSource
from discord.ext import commands
from discord import app_commands
import discord
import asyncio
import re


class InvalidQueryException(Exception):
    """Raised when the query is empty or None"""
    pass


id = "1044552464382308372"

class Play(commands.Cog):
    def __init__ (self, client: commands.Bot) -> None:
        self.client = client
        self.servers = {}
        
    async def create_embed(self, ctx, result) -> discord.Embed:    
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
        
        song_embed.set_footer(text=f"\nRequesed by {ctx.message.author.display_name}", icon_url=ctx.message.author.display_avatar)
    
        return song_embed
    
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.voice_client.guild.change_voice_state(channel=channel, self_deaf=True)
        else:
            raise commands.CommandError("Author not connected to voice channel.")
        
    async def handle_skip(self, ctx, error):
        if error:
            print(error)
        elif self.servers[ctx.voice_client.guild.id]:
            await self.play_next(ctx)
        
    async def play_next(self, ctx):
        self.servers[ctx.voice_client.guild.id].pop(0)
        
        if self.servers[ctx.voice_client.guild.id]:
            ctx.voice_client.play(self.servers[ctx.voice_client.guild.id][0]['song'], after=lambda e=None: self.client.loop.create_task(self.handle_skip(ctx, e)))
            
            song_embed = self.servers[ctx.voice_client.guild.id][0]['embed']
            song_embed.set_author(name="Now Playing")
            song_embed.set_field_at(3, name='Position in queue', value=f"`{len(self.servers[ctx.voice_client.guild.id])}`")  
            
            await ctx.send(embed = song_embed)
        else:
            await ctx.send("> No songs in queue")  
            
    @commands.command()
    async def skip(self, ctx):
        if self.servers[ctx.voice_client.guild.id]:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
        else:
            await ctx.send("> No songs in queue")
        
    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        
    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        
    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
    
    @commands.command()
    async def play(self, ctx):
        try:
            async with ctx.typing():
                query = ' '.join(re.sub('play', '', ctx.message.content).split(' ')[1:])
                
                if (query == ' ' or query == '' or query == None): 
                    raise InvalidQueryException
                else:
                    result = YTDLSource.search(query=query)                    
                    song_embed = await self.create_embed(ctx=ctx, result=result)
                    
                    source = await YTDLSource.stream(loop=self.client.loop, url=result['link'])
                    
                    if not ctx.voice_client:
                        await self.join(ctx=ctx)
                        
                    if not ctx.voice_client.is_playing():
                        song_embed.set_author(name="Now Playing")
                        self.servers[ctx.voice_client.guild.id] = [{'song': source, 'embed': song_embed, 'count': 1, 'by': ctx.author.id}]
                        
                        ctx.voice_client.play(self.servers[ctx.voice_client.guild.id][0]['song'], after=lambda e=None: self.client.loop.create_task(self.handle_skip(ctx, e)))
                    
                    else:
                        song_embed.set_author(name="Added to queue")
                        self.servers[ctx.voice_client.guild.id].append({'song': source, 'embed': song_embed, 'count': 1, 'by': ctx.author.id})
                    
                    song_embed.add_field(name='Position in queue', value=f"`{len(self.servers[ctx.voice_client.guild.id])}`")    
                    await ctx.send(embed = song_embed)
                        
        except InvalidQueryException:
            await ctx.send("> `play` command must contain an argument ❌")
        except commands.CommandError:
            await ctx.send("> You are not connected to a voice channel")
    
    @app_commands.command(name='play', description="play's songs as per your request")
    async def _play(self, ctx: discord.Interaction):
        song_embed = await self.create_embed(ctx=ctx)
        await ctx.response.send_message(embed=song_embed)
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Play(bot))
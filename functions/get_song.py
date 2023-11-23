from youtubesearchpython import VideosSearch
from discord.ext import commands
import yt_dlp as youtube_dl
import discord
import asyncio


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, data, volume: float = 1):
        super().__init__(source, volume)
        
        self.data = data
        self.title = data.get('title')

    @classmethod
    def search(self, query: str) -> dict:
        search = VideosSearch(query, limit=1)
        return search.result()['result'][0]

    @classmethod
    async def stream(cls, url, loop=None):        
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url=url, download=False))
        
        return cls(source=discord.FFmpegPCMAudio(data['url'], **ffmpeg_options), data=data)
    
# print(search('never have i felt like this'))
            
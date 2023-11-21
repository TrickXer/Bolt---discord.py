from youtubesearchpython import VideosSearch
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
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, data, volume: float = 1):
        super().__init__(source, volume)
        
        self.data = data
        self.title = data.get('title')


    def search(self, query: str) -> dict:
        search = VideosSearch(query, limit=1)
        return search.result()['result'][0]

    @classmethod
    def stream(cls, self, loop=None, query: str = 'Never have I felt like this'):
        result = self.search(query=query)
        
        loop = loop or asyncio.get_event_loop()
        data = loop.run_in_executor(None, lambda: ytdl.extract_info(url=result['link'], download=False))
        
        return cls(source=discord.FFmpegPCMAudio(data['url'], **ffmpeg_options), data=data)
    

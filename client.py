from discord.ext import commands
import logging
import discord
import dotenv
import os


dotenv.load_dotenv(dotenv_path="bolt-env/.env")

log = logging.getLogger("discord")

class Client(commands.Bot):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ready(self) -> None:
        log.info(f"Logged in as {self.user}")
        
    async def setup_hook(self) -> None:
        for cmd in os.listdir('commands'):
            if not cmd.startswith('_') and cmd.endswith('.py'):
                await self.load_extension(f"commands.{cmd[:-3]}")
                
    async def on_connect(self) -> None:
        synced_cmds = await self.tree.sync()
        log.info(f"Successfully synced {len(synced_cmds)}")
        
intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix=os.getenv('CMD_PREFIX'), intents=intents)
client.remove_command('help')
client.run(os.getenv('TOKEN'))

from pyrogram import Client
from pyrogram.enums import ParseMode
from datetime import datetime
from configs import Config
from aiohttp import web
import os
from plugins import web_server
import asyncio 
import logging
from logging.handlers import RotatingFileHandler

# Set the log file name
LOG_FILE_NAME = "Rkbotz_log_file.log"

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

PORT = int(os.environ.get('PORT', 8080))

class Bot(Client):
    def __init__(self):
        super().__init__(
            name=Config.BOT_USERNAME,
            api_hash=Config.API_HASH,
            api_id=Config.API_ID,
            plugins={"root": "plugins"},
            bot_token=Config.BOT_TOKEN
        )
        self.LOGGER = LOGGER(__name__)

    async def start(self):
        await super().start()        
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER.info("Bot Running..!\n\nCreated by \nhttps://t.me/Rk_botz")
        self.LOGGER.info(""" \n\n
        # (©)Rk_botz
        """)

        self.username = usr_bot_me.username

        
        # web-response
        app = web.Application()
        app.add_routes([web.get('/', self.handle)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', PORT)
        await site.start()

    async def handle(self, request):
        return web.Response(text="Hello, world")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER.info("Bot stopped.")

    

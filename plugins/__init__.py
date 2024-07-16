# (c) github - @Rishikesh-Sharma09 ,telegram - https://telegram.me/Rk_botz
# removing credits dont make you coder 

from aiohttp import web
from .route import routes


async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

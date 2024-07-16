# (c) github - @Rishikesh-Sharma09 ,telegram - https://telegram.me/Rk_botz
# removing credits dont make you coder 

from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("Rkbotz")

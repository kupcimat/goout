from aiohttp import web


def create_routes():
    return [web.get("/", hello)]


async def hello(request):
    return web.Response(text="Hello, world")

import logging
import os

from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


logging.basicConfig(level=logging.DEBUG)
port = int(os.getenv("PORT", default=8080))

app = web.Application()
app.add_routes([web.get("/", hello)])

web.run_app(app, port=port)

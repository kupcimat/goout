import logging
import os

from aiohttp import web

from kupcimat import routes

logging.basicConfig(level=logging.DEBUG)
port = int(os.getenv("PORT", default=8080))

app = web.Application()
app.add_routes(routes.create_routes())

web.run_app(app, port=port)

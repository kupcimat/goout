import logging

from aiohttp import web

from kupcimat.web import config
from kupcimat.web import routes

logging.basicConfig(level=logging.DEBUG)

app = web.Application()
app.add_routes(routes.create_routes())

web.run_app(app, port=config.PORT)

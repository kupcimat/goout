from typing import List

from aiohttp import web


def create_routes() -> List[web.RouteDef]:
    return [
        web.get("/api", hello)
    ]


async def hello(request: web.Request) -> web.Response:
    return web.json_response({})

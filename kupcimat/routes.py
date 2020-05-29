import uuid
from typing import List

from aiohttp import web

from kupcimat import storage

BUCKET_NAME = "goout-test"


def create_routes() -> List[web.RouteDef]:
    return [
        web.get("/api/files/uploadLink", get_upload_url),
        web.get("/api/files/{file_name}/downloadLink", get_download_url)
    ]


async def get_upload_url(request: web.Request) -> web.Response:
    url = storage.generate_upload_signed_url(BUCKET_NAME, uuid.uuid4().hex)
    response = {
        "upload": {
            "url": url,
            "curl": storage.generate_upload_curl(url)
        }
    }
    return web.json_response(response)


async def get_download_url(request: web.Request) -> web.Response:
    file_name = request.match_info["file_name"]
    url = storage.generate_download_signed_url(BUCKET_NAME, file_name)
    response = {
        "download": {
            "url": url,
            "curl": storage.generate_download_curl(url)
        }
    }
    return web.json_response(response)

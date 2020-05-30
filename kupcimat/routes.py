from typing import List

from aiohttp import web

from kupcimat import storage
from kupcimat import util
from kupcimat.routes_util import created, moved

BUCKET_NAME = "goout-test"


def create_routes() -> List[web.RouteDef]:
    return [
        web.post("/api/files", create_upload_url),
        web.get("/api/files/{file_id}", download_file),
        web.post("/api/files/{file_id}/tasks", create_task),
        web.get("/api/files/{file_id}/tasks/{task_id}", get_task)
    ]


async def create_upload_url(request: web.Request) -> web.Response:
    file_id = util.generate_id()
    url = storage.generate_upload_signed_url(BUCKET_NAME, file_id)
    response = {
        "file": {
            "id": file_id,
            "uploadUrl": url,
            "uploadCurl": storage.generate_upload_curl(url)
        }
    }
    return web.json_response(response, **created(f"/api/files/{file_id}"))


async def download_file(request: web.Request) -> web.Response:
    file_id = request.match_info["file_id"]
    url = storage.generate_download_signed_url(BUCKET_NAME, file_id)
    return web.Response(**moved(url))


async def create_task(request: web.Request) -> web.Response:
    # TODO check file existence
    # TODO create task for worker
    file_id = request.match_info["file_id"]
    task_id = util.generate_id()
    response = {
        "task": {
            "id": task_id
        }
    }
    return web.json_response(response, **created(f"/api/files/{file_id}/tasks/{task_id}"))


async def get_task(request: web.Request) -> web.Response:
    # TODO check file and task existence
    file_id = request.match_info["file_id"]
    task_id = request.match_info["task_id"]
    response = {
        "task": {
            "id": task_id,
            "result": 42
        }
    }
    return web.json_response(response)

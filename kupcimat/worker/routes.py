from typing import List

from aiohttp import web

from kupcimat.routes_util import created, path_variables


def create_routes() -> List[web.RouteDef]:
    return [
        web.post("/api/tasks", create_task),
        web.get("/api/tasks/{task_id}", get_task)
    ]


async def create_task(request: web.Request) -> web.Response:
    # TODO validate json input
    task_json = await request.json()
    task_id = task_json["task"]["id"]
    response = {
        "task": {
            "id": task_id
        }
    }
    return web.json_response(response, **created(f"/api/tasks/{task_id}"))


async def get_task(request: web.Request) -> web.Response:
    # TODO check task existence
    task_id = path_variables(request, "task_id")
    response = {
        "task": {
            "id": task_id,
            "result": 42
        }
    }
    return web.json_response(response)

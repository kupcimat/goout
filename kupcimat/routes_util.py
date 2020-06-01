from typing import Any, Dict, List, Union

from aiohttp import web


def created(location: str) -> Dict[str, Any]:
    return {
        "status": 201,
        "headers": {"Location": location}
    }


def moved(location: str) -> Dict[str, Any]:
    return {
        "status": 301,
        "headers": {"Location": location}
    }


def path_variables(request: web.Request, *variables: str) -> Union[str, List[str]]:
    if len(variables) == 1:
        return request.match_info[variables[0]]
    return [request.match_info[variable] for variable in variables]


def json_get(json: Any, *path: str) -> Any:
    if len(path) == 0:
        return json
    if path[0] in json:
        return json_get(json[path[0]], *path[1:])
    raise web.HTTPBadRequest(reason="Invalid payload")

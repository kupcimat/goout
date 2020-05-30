from typing import Any, Dict, List, Union

from aiohttp import web


def path_variables(request: web.Request, *variables: str) -> Union[str, List[str]]:
    if len(variables) == 1:
        return request.match_info[variables[0]]
    return [request.match_info[variable] for variable in variables]


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

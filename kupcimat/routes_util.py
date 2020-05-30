from typing import Dict, Any


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

from typing import Dict, Any


def created(location: str) -> Dict[str, Any]:
    return {
        "status": 201,
        "headers": {"Location": location}
    }

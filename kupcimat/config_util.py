import os
from typing import Optional


def get_str(variable: str, default: Optional[str] = None) -> str:
    value = os.getenv(variable, default)
    if value is None:
        raise RuntimeError(f"Environment variable {variable} is not set")
    return value


def get_int(variable: str, default: Optional[int] = None) -> int:
    return int(get_str(variable, default))

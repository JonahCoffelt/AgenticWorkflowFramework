from typing import Any


def validate_int(data: int|float) -> int:
    if isinstance(data, (int, float)):
        return int(data)
    raise ValueError(f'Framework: Expected an int, got type {type(data)}')

def validate_float(data: int|float) -> float:
    if isinstance(data, (int, float)):
        return float(data)
    raise ValueError(f'Framework: Expected an float, got type {type(data)}')

def validate_string(data: str) -> str:
    if isinstance(data, str):
        return data
    raise ValueError(f'Framework: Expected an string, got type {type(data)}')

def validate_bool(data: bool) -> bool:
    if isinstance(data, bool):
        return data
    raise ValueError(f'Framework: Expected an bool, got type {type(data)}')
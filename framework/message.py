from typing import Any


class Message:
    """Data sent across the server from one node to another"""
    sender: tuple[str, int]
    receivers: list[tuple[str, int]]

    @property
    def receivers(self) -> list[tuple[str, int]]: 
        return self._receivers

    @receivers.setter
    def receivers(self, value: list[tuple[str, int]]):
        if not isinstance(value, list): 
            value = [value]
        self._receivers = value

class Request(Message):
    """Expect a response from the other side"""
    method: str
    params: dict[str, Any] | None

    def __init__(self, method: str, **params: Any) -> None:
        self.method = method
        self.params = params


class Result(Message):
    """Successful responses to requests"""
    key: str
    value: Any

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value


class Error(Message):
    """Indicate that a request failed"""
    code: int
    message: str
    data: Any | None
    value: Any | None

    def __init__(self, code: int, message: str, data: Any | None=None) -> None:
        self.code = code
        self.message = message
        self.data = data
        self.value = None


class Notification(Message):
    """One-way messages that dont expect a response"""
    method: str
    params: dict[str, Any] | None

    def __init__(self, method: str, **params: Any) -> None:
        self.method = method
        self.params = params
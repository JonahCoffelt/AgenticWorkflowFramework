from typing import Any, Optional


class Message:
    sender: tuple[str, int]
    recivers: list[tuple[str, int]]

    @property
    def recivers(self): return self._recivers

    @recivers.setter
    def recivers(self, value):
        if not isinstance(value, list): value = [value]
        self._recivers =  value


class Request(Message):
    method: str
    params: Optional[dict]

    def __init__(self, method: str, **params) -> None:
        """Expect a response from the other side"""
        self.method = method
        self.params = params


class Result(Message):
    key: str
    value: Any

    def __init__(self, key: str, value: Any) -> None:
        """Successful responses to requests"""
        self.key = key
        self.value = value


class Error(Message):
    code: int
    message: str
    data: Optional[Any]

    def __init__(self, code: int, message: str, data: Optional[Any]=None) -> None:
        """Indicate that a request failed"""
        self.code = code
        self.message = message
        self.data = data


class Notification(Message):
    method: str
    params: Optional[dict]

    def __init__(self, method: str, **params) -> None:
        """One-way messages that dont expect a response"""
        self.method = method
        self.params = params
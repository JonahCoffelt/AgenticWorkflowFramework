from typing import Any
from .data_validation import validate_string
from .networking.client import Client
from .message import Request, Notification


class Resource(Client):
    """Implementation of a resource class that synchronizes with the context."""
    
    name: str
    value: Any
    
    def __init__(self, name: str, value: Any) -> None:
        """
        Container for a single resource in the context.
        Essentially stored as a key-value pair.

        Args:
            name (str): Used to identify the resource.
            value (Any): data of the resource.
        """
        super().__init__()

        self.name = name
        self.value = value

    @property
    def name(self) -> str: 
        return self._name
    @property
    def value(self) -> Any: 
        self._value = self.send(Request("get resource", name=self.name)).value
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value
        self.send(Notification("set resource", name=self.name, value=value))
    @name.setter
    def name(self, value: str) -> None:
        self._name = validate_string(value)

    def __repr__(self) -> str:
        return f'<Resource | {self.name} : {self.value} >'
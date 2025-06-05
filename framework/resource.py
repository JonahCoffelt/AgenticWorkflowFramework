import pickle
from typing import Any
from .data_validation import validate_string
from .networking.client import Client
from .networking.network_node import IP, PORT
from .message import Request, Result, Notification, Message


class Resource(Client):
    name: str
    """"""
    value: Any
    """"""
    
    def __init__(self, name: str, value: Any):
        """
        Container for a single resource in the context.
        Essentially stored as a key-value pair. 
        Args:
            name: str
                Used to identify the resource
            value
        """
        super().__init__()

        self.name = name
        self.value = value

    def send(self, message: Message) -> Result | None:

        message.sender = self.address
        message.receivers = [(IP, PORT)]

        if isinstance(message, Request): self.hold = True

        super().send(pickle.dumps(message))

        # Get result if needed
        if isinstance(message, Request): 
            self.await_result()
            return self.recent_result

    @property
    def name(self) -> str: return self._name
    @property
    def value(self) -> Any: 
        self._value = self.send(Request("get resource", name=self.name)).value
        return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value
        self.send(Notification("set resource", name=self.name, value=value))
    @name.setter
    def name(self, value: str):
        self._name = validate_string(value)

    def __repr__(self):
        return f'<Resource | {self.name} : {self.value} >'
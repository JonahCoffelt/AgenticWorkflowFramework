import pickle
from typing import Any
from .data_validation import validate_string
from .networking.client import Client
from .networking.network_node import IP, PORT
from .message import Request, Notification, Message


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
        
        self.methods = {
            "get resource" : self.get_resource
        }

        self.name = name
        self.value = value

    def send(self, message: Notification) -> Message:

        message.sender = self.address
        message.recivers = [(IP, PORT)]

        super().send(pickle.dumps(message))

        return message

    def get_resource(self, name: str, value: Any):
        """Called when a request result comes in for get resource"""
        self._value = value

    def sync(self):
        """Syncs data with the context. Pauses operation until data is recived"""
        self.await_response(self.send(Request("get resource", name=self.name)))

    @property
    def name(self) -> str: return self._name
    @property
    def value(self) -> Any: 
        self.sync()
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
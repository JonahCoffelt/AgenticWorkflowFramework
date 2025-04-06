import json
from typing import Any


class Message:
    content: str
    """The message content. Typically the actual message itself"""
    resources: list[Any]
    """The resources of the message (typically used for args or returns)"""
    type: str
    """The type of message this is (inform, tool, request)"""
    sender: int
    """ID of the sender agent"""
    recivers: list[int]
    """List of IDs of reciver agents"""


    def __init__(self, content: str=None, resources: list[Any]=[], type: str='inform', sender: int=0, recivers: list[int]=[]):
        """
        Container for all the data and functionality of a message's data
        """

        self._data = {}
        self._data['content']   = content
        self._data['resources'] = resources
        self._data['type']      = type
        self._data['sender']    = sender
        self._data['recivers']  = recivers

    # Getters
    @property
    def content(self) -> str:
        """The message content. Typically the actual message itself"""
        return self._data['content']

    @property
    def resources(self) -> list[Any]:
        """The resources of the message (typically used for args or returns)"""
        return self._data['resources']
    
    @property
    def type(self) -> str:
        """The type of message this is (inform, tool, request)"""
        return self._data['type']
    
    @property
    def sender(self) -> int:
        """ID of the sender agent"""
        return self._data['sender']
    
    @property
    def recivers(self) -> list[int]:
        """List of IDs of reciver agents"""
        return self._data['recivers']
    
    @property
    def data(self):
        """The json dumped data of the message. Used for sending"""

        return json.dumps(self._data)

    # Setters
    @content.setter
    def content(self, value: str) -> None:
        self._data['content'] = value

    @resources.setter
    def resources(self, value: list[Any]) -> None:
        self._data['resources'] = value

    @type.setter
    def type(self, value: str) -> None:
        self._data['type'] = value

    @sender.setter
    def sender(self, value: int) -> None:
        self._data['sender'] = value

    @recivers.setter
    def recivers(self, value: list[int]) -> None:
        self._data['recivers'] = value
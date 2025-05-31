import pickle
from typing import Optional
from .network_node import NetworkNode, IP, PORT
from ..message import Message, Request, Result, Error, Notification
import time

class ContextNode(NetworkNode):
    def __init__(self, ip: str=IP, port: int=PORT):
        super().__init__(ip, port)
        self.methods = {}
        self.hold = False
        self.recent_result = None

    def receive(self, data: bytes, address: tuple[str, int]) -> None:
        """Processes a recived message."""

        message: Message = pickle.loads(data)
        self.handle_message(message)

    def add_tool(self, name: str, function) -> None:
        """Adds a new tool to the node"""
        self.methods[name] = function

    def await_result(self):
        """Waits until the message has recived a reponse"""
        while self.hold: ...

    def handle_message(self, message: Message) -> Optional[Result | Error]:
        """Matches the message type to the correct method for handling it"""
        match type(message).__name__:
            case Request.__name__:
                self.handle_request(message)
            case Result.__name__:
                self.handle_result(message)
            case Error.__name__:
                self.handle_error(message)
            case Notification.__name__:
                self.handle_notification(message)
            case _:
                print("Context recived invalid Message type: {type(message)}")

    def call_method(self, message) -> Optional[dict]:
        """Calls a method from a request or notification. Returns the result"""
        # Get data from the message
        method = message.method
        params = message.params

        # Verify valid method request
        if method not in self.methods:
            return Error(5, f"Got invalid method identifier: {method}")
        
        # Call the method and get result
        try:
            result = self.methods[method](**params)
        except TypeError:
            return Error(6, f"Got invalid method parameters for {method}: {params}")
        
        return result

    def handle_request(self, message: Request) -> Result | Error:
        """"""

        # Call the method given in the message
        result = self.call_method(message)
        self.send(result, message.sender)

    def handle_result(self, message: Result) -> None:
        """"""
        self.recent_result = message
        self.hold = False

    def handle_error(self, message: Error) -> None:
        """"""
        self.recent_result = message
        self.hold = False
        print(f"Error {message.code}: {message.message}")

    def handle_notification(self, message: Notification) -> None:
        """"""

        # Call the method given in the message
        self.call_method(message)
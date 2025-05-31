import pickle
from typing import Optional
from .network_node import NetworkNode, IP, PORT
from ..message import Message, Request, Result, Error, Notification


class ContextNode(NetworkNode):
    def __init__(self, ip: str=IP, port: int=PORT):
        super().__init__(ip, port)
        self.methods = {}
        self.holds = set()

    def receive(self, data: bytes, address: tuple[str, int]) -> None:
        """Processes a recived message."""

        message: Message = pickle.loads(data)
        self.handle_message(message)

    def await_response(self, message: Request | Notification):
        """Waits until the message has recived a reponse"""
        self.holds.add(message.method)
        while message.method in self.holds: ...

    def handle_message(self, message: Message) -> None:
        """Matches the message type to the correct method for handling it"""
        match type(message).__name__:
            case Request.__name__:
                self.handle_request(message)
                if message.method in self.holds: self.holds.remove(message.method)
            case Result.__name__:
                self.handle_result(message)
            case Error.__name__:
                self.handle_error(message)
            case Notification.__name__:
                self.handle_notification(message)
                if message.method in self.holds: self.holds.remove(message.method)
            case _:
                print("Context recived invalid Message type: {type(message)}")

    def call_method(self, message) -> Optional[dict]:
        """Calls a method from a request or notification. Returns the result"""
        # Get data from the message
        method = message.method
        params = message.params

        # Verify valid method request
        if method not in self.methods:
            print(f"Got invalid method identifier: {method}")
            return None
        
        # Call the method and get result
        try:
            result = self.methods[method](**params)
        except TypeError:
            print(f"Got invalid method parameters for {method}: {params}")
            return None
        
        return result

    def handle_request(self, message: Request) -> None:
        """"""

        # Call the method given in the message
        result = self.call_method(message)

        # Check if the call resulted in an error
        if isinstance(result, Error):
            self.send(result, message.sender)
            return

        # Return the result to the agent that called
        self.send(Notification(message.method, **result), message.sender)

    def handle_result(self, message: Result) -> None:
        """"""
        ...

    def handle_error(self, message: Error) -> None:
        """"""
        print(f"Error {message.code}: {message.message}")

    def handle_notification(self, message: Notification) -> None:
        """"""

        # Call the method given in the message
        self.call_method(message)
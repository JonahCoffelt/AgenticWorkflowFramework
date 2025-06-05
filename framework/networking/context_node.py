import pickle
from threading import Event
from .network_node import NetworkNode, IP, PORT
from ..message import Message, Request, Result, Error, Notification

class ContextNode(NetworkNode):
    """Class for creating nodes in the MCP system, including the context, agents, and resources"""
    
    methods: dict[str, callable]
    hold: bool
    recent_result: Result | Error | None

    def __init__(self, ip: str=IP, port: int=PORT) -> None:
        """
        Initializes the network node, binds the socket, and starts a listen thread.

        Args:
            ip (str): The IP address to host the socket on. Defaults to '127.0.0.1'.
            port (int): The port number to host the socket on. Defaults to 5051.
        """

        super().__init__(ip, port)

        # Dictionary of availible methods
        self.methods = {}

        # Initalize state attributes
        self.hold = False
        self._result_event = Event() 
        self.recent_result = None

    def receive(self, data: bytes, address: tuple[str, int]) -> None:
        """Processes a received message."""

        message: Message = pickle.loads(data)
        self.handle_message(message)

    def add_tool(self, name: str, function: callable) -> None:
        """Adds a new tool to the node"""
        self.methods[name] = function

    def await_result(self):
        """Waits until the message has recived a reponse"""
        while self.hold: ...

    def handle_message(self, message: Message) -> Result | Error | None:
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

    def call_method(self, message) -> dict | None:
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
        """
        Calls the method in the request and sends back the results
        Args:
            message (Request): 
        """

        # Call the method given in the message
        result = self.call_method(message)
        result.receivers = (IP, PORT)
        result.sender = self.address
        self.send(result, message.sender)

    def handle_result(self, message: Result) -> None:
        """
        Saves the result and releases any hold on the node
        Args:
            message (Result): 
        """

        self.recent_result = message
        self.hold = False

    def handle_error(self, message: Error) -> None:
        """
        Saves the result and releases any hold on the node
        Args:
            message (Error): 
        """

        self.recent_result = message
        self.hold = False
        print(f"Error {message.code}: {message.message}")

    def handle_notification(self, message: Notification) -> None:
        """
        Calls the method in the notification. Sends back an error if one occurs
        Args:
            message (Notification): 
        """

        # Call the method given in the message
        result = self.call_method(message)

        # Send an error if one occurs, otherwaise, no need to respond to notification
        if isinstance(result, Error):
            result.receivers = (IP, PORT)
            result.sender = self.address
            self.send(result)
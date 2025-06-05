import pickle
from threading import Event
from .network_node import NetworkNode, IP, PORT
from ..message import Message, Request, Result, Error, Notification

class Node(NetworkNode):
    """Class for creating nodes in the MCP system, including the context, agents, and resources."""
    
    methods: dict[str, callable]
    recent_result: Result | Error | None

    def __init__(self, ip: str=IP, port: int=PORT) -> None:
        """
        Initializes the network node, binds the socket, and starts a listen thread.

        Args:
            ip (str): The IP address to host the socket on. Defaults to '127.0.0.1'.
            port (int): The port number to host the socket on. Defaults to 5051.
        """

        super().__init__(ip, port)

        # Dictionary of available methods
        self.methods = {}

        # Initialize state attributes
        self._result_event = Event() 
        self.recent_result = None

    def send(self, message: Message, receivers: list[tuple[str, int] | NetworkNode] | tuple[str, int] | NetworkNode=(IP, PORT)) -> Result | None:
        """
        Sends the given message to the receivers. 
        If the message is a request, it awaits a reponse and returns it.
        Args:
            message (Message): The message to be sent
            receivers (list[tuple[str, int]): List of addresses for the message to be sent to
        """
        
        # Ensure correct message data before send
        message.sender = self.address
        message.receivers = receivers

        # Send the message to context to distribute to all receivers

        self.send_bytes(pickle.dumps(message))

        # Get result if needed
        if isinstance(message, Request): 
            self.await_result()
            return self.recent_result
        
    def receive(self, data: bytes, address: tuple[str, int]) -> None:
        """Processes a received message."""
        message: Message = pickle.loads(data)
        self.handle_message(message, address)

    def await_result(self):
        """Waits until a result has been received and processed."""
        self._result_event.wait()
        self._result_event.clear()
    
    def add_tool(self, name: str, function: callable) -> None:
        """Adds a new tool to the node."""
        self.methods[name] = function

    def call_tool(self, name: str, receiver=(IP, PORT), **params) -> Result | Error | None:
        """Invokes a local tool (method) or sends a Request message to a remote node to call a tool."""
        request = Request(name, **params)
        if receiver == self.address: return self.call_method(request)
        return self.send(request, receivers=receiver)

    def handle_message(self, message: Message, address: tuple[str, int]) ->  None:
        """Matches the message type to the correct method for handling it."""
        match type(message).__name__:
            case Request.__name__:
                self.handle_request(message, address)
            case Result.__name__:
                self.handle_result(message, address)
            case Error.__name__:
                self.handle_error(message, address)
            case Notification.__name__:
                self.handle_notification(message, address)
            case _:
                print(f"Context received invalid Message type: {type(message).__name__}")

    def call_method(self, message: Request | Notification, address: tuple[str, int]=None) -> Result | Error | None:
        """Calls a method from a request or notification. Returns the result."""
        # Get data from the message
        method = message.method
        params = message.params

        # Verify valid method request
        if method not in self.methods:
            return Error(5, f"Got invalid method identifier: {method}")
        
        # Call the method and return result
        try:
            
            result = self.methods[method](**params)
            return result
        except TypeError:
            return Error(6, f"Got invalid method parameters for {method}: {params}")
        
    def handle_request(self, message: Request, address: tuple[str, int]=None) -> None:
        """
        Calls the method in the request and sends back the results.
        Args:
            message (Request): The Request message containing the method and parameters to call.
        """

        # Call the method given in the message
        result = self.call_method(message, address)
        self.send(result, message.sender)

    def handle_result(self, message: Result, address: tuple[str, int]=None) -> None:
        """
        Saves the result and releases any hold on the node.
        Args:
            message (Result): The Result message containing the successful response data.
        """
        self.recent_result = message
        self._result_event.set()

    def handle_error(self, message: Error, address: tuple[str, int]=None) -> None:
        """
        Saves the result and releases any hold on the node.
        Args:
            message (Error): The Error message containing details about the failed request.
        """

        self.recent_result = message
        self._result_event.set()
        print(f"Error {message.code}: {message.message}")

    def handle_notification(self, message: Notification, address: tuple[str, int]=None) -> None:
        """
        Calls the method in the notification. Sends back an error if one occurs.
        Args:
            message (Notification): The Notification message containing the method and parameters.
        """

        # Call the method given in the message
        result = self.call_method(message, address)

        # Send an error if one occurs, otherwaise, no need to respond to notification
        if isinstance(result, Error):
            self.send(result, message.sender)
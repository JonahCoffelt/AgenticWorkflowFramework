import pickle
from .networking.client import Client
from .networking.network_node import NetworkNode, IP, PORT
from .message import Message, Request, Result, Error, Notification


class Agent(Client):
    def __init__(self):
        super().__init__()
 
        self.methods = {
            "message" : self.message
        }

        # Register with the context
        self.is_registered = self.send(Request("register", address=self.address)).value

    def send(self, message: Message, recivers: list[tuple[str, int] | NetworkNode] | tuple[str, int] | NetworkNode=(IP, PORT)) -> Result | None:
        """
        Sends the given message to the recivers. If the message is a request, it awaits a reponse and returns it.
        """
        
        # Add data to the message
        message.sender = self.address
        message.recivers = recivers

        if isinstance(message, Request): self.hold = True

        # Send to context to distribute
        super().send(pickle.dumps(message))

        # Get result if needed
        if isinstance(message, Request): 
            self.await_result()
            return self.recent_result

    def call_tool(self, name: str, reciver=(IP, PORT), **params) -> Result:
        """Wrapper for the send command that calls a tool"""
        if reciver == self.address: return self.call_method(Request(name, **params))
        return self.send(Request(name, **params), recivers=reciver)

    #######################################################################
    #                          Internal Methods                           #
    #######################################################################

    def message(self, content: str) -> Result:
        print(f"Agent {self.address} recived message: {content}")
        Result("recived", True)
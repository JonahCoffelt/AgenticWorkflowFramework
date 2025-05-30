import pickle
from .networking.client import Client
from .networking.network_node import NetworkNode, IP, PORT
from .message import Message, Request, Result, Error, Notification


class Agent(Client):
    def __init__(self):
        super().__init__()

        self.is_registered = False

        self.methods = {
            "register" : self.register
        }

        self.send(Request("register", {"address": self.address}))

    def send(self, message: Message, recivers: list[tuple[str, int] | NetworkNode] | tuple[str, int] | NetworkNode=(IP, PORT)):

        message.sender = self.address
        message.recivers = recivers

        for reciver in message.recivers:
            super().send(pickle.dumps(message), reciver)

    # Following methods are interanlly provided tools for the agents

    def register(self, registered: bool) -> None:
        self.is_registered = registered
    def deregister(self, registered: bool) -> None:
        self.register(registered)
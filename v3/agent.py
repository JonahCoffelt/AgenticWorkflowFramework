import json
from threading import Thread
from .messenger import Messenger
from .client import Client
from .message import Message


class Agent(Messenger):
    def __init__(self):
        super().__init__()

        # Create the client
        self.server = Client(self.recive)
        self.identifier = 0

        # Tools
        self.tools['register'] = self.register

        # Tread for the control channel
        thread = Thread(target=self.start)
        thread.start()

        # Reister this agent with the server
        register_request = Message(content='register', type='tool')
        self.send(register_request)

    def register(self, address, identifier: int):
        print(f'Registered with id {identifier}')
        self.identifier = identifier

    def __repr__(self) -> str:
        return f'<Agent | id: {self.identifier}>'
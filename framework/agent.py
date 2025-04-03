import json
from threading import Thread
from .messenger import Messenger
from .client import Client


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
        self.send(content='register', type='tool')

    def register(self, address, identifier: int):
        print(f'Registered with id {identifier}')
        self.identifier = identifier

    def __repr__(self) -> str:
        return f'<Agent | id: {self.identifier}>'
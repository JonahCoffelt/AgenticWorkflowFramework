import json
from threading import Thread
from .client import Client


class Agent:
    identifier: int
    """Unique global identifier for the agent"""
    role: str
    """The role the agent plays in the context. Serves as a permision level"""
    type: str
    """Either AI or human"""

    def __init__(self):
        """
        
        """

        self.client = Client()
        self.identifier = 0

        self.identifier = int(self.send('{"tool" : "register", "args" : []}', type='request'))

    # def start_loop(self):
    #     self.running = True
    #     while self.running:
    #         try:
    #             if self.do_listen: self.client.listen()
    #         except KeyboardInterrupt:
    #             self.running = False

    def listen(self) -> None:
        print('got: ', self.client.listen())

    def message(self, message: str):
        """
        Sends a message to this agent from the context
        """

        message = json.loads(message)
        print(f'recived : {message}')

    def send(self, message: str, recivers: list[int]=[], type: str='inform') -> str:
        """
        Sends a message to the context from this agent
        """

        # Format the message 
        data = {}
        data['type']     = type
        data['sender']   = self.identifier
        data['recivers'] = recivers
        data['content']  = message

        # Convert to json string
        data = json.dumps(data)

        # Send to the context
        return self.client.send(data)

    def __repr__(self) -> str:
        return f'<Agent | id: {self.identifier}>'
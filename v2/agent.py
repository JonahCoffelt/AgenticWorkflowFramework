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

        # self.identifier = int(self.send('{"tool" : "register", "args" : []}', type='request'))
        self.send('{"tool" : "register", "args" : []}', type='request')

        # TODO Maybe have a control channel
        thread = Thread(target=self.start)
        thread.start()

    def start(self):
        """
        
        """
        
        print('Context server starting')

        self.running = True
        while self.running:
            result = None
            try:
                result = self.client.listen()
            except KeyboardInterrupt:
                self.running = False

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

    def recive(self, data: str, address=None) -> str:
        """
        
        """

        match json.loads(data)['type']:
            case 'inform':
                return self.send(data)
            case 'request':
                return self.request(data, address)
            case _:
                print('unrecognized message type')
                return 'None'

    def request(self, data: str, address: ...) -> str:
        """
        Request the use of a tool in the context
        """

        # Load data and tool data    
        data = json.loads(data)
        tool_data = json.loads(data['content'])
    
        # Get the tool and the arguments 
        func = self.tools[tool_data['tool']]
        args = tool_data['args']
        
        # Call the tool
        return func(address, *args)

    def __repr__(self) -> str:
        return f'<Agent | id: {self.identifier}>'
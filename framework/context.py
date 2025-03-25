import json
from .server import Server
from .agent import Agent


class Context:
    def __init__(self):
        """
        Defines the enviornment in which agents interact
        """
        
        # Agent attributes
        self.agents = {}
        self.available_id = 0

        # Tools
        self.tools = {}
        self.tools['register'] = self.register
        self.tools['deregister'] = self.deregister

        # Create and start the server for reciving messages
        self.server = Server(self.recive)

    def start(self):
        """
        
        """
        
        print('Context server starting')

        self.running = True
        while self.running:
            try:
                self.server.update()
            except KeyboardInterrupt:
                self.running = False

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

    def send(self, message: str) -> str:
        """
        Send a message to interact with the context
        """

        message = json.loads(message)

        for reciver in message['recivers']:
            agent = self.agents[reciver]
            agent.message(json.dumps(message))

        return 'Recived Message'

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

    def register(self, address: ...) -> int:
        """
        Adds an agent to the context
        """

        print(f'registering agent at {address}')

        # Add to the dict of agents
        self.agents[self.available_id] = address

        # Inc
        self.available_id += 1

        return str(self.available_id - 1)

    def deregister(self, agent: Agent):
        """
        Removes an agent from the context
        """

        del self.agents[agent.identifier]
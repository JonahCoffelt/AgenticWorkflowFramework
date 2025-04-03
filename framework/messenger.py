import json


class Messenger:
    def __init__(self):
        """
        Abstract class used to implement the agent and the context.
        Allows for interaction between network users.
        """
        
        self.tools = {}
        self.events = []

    def start(self):
        """
        Starts the server
        """
        
        print('Starting')

        self.running = True
        while self.running:
            try:
                self.server.listen()
            except KeyboardInterrupt:
                self.running = False

    def recive(self, data: str, address=None) -> str:
        """
        Recives a data from the server and sends it to the correct function to handle it
        """
        
        match json.loads(data)['type']:
            case 'inform':
                return self.inform(data, address)
            case 'tool':
                return self.tool(data, address)
            case _:
                print('unrecognized message type')
                return 'None'

    def send(self, ip: str=None, port: int=None, content: str='', data=[], recivers: list[int]=[], type: str='inform') -> str:
        """
        Sends a message to the given ip
        """

        # Format the message 
        message = {}
        message['content']  = content
        message['data']     = data
        message['recivers'] = recivers
        message['type']     = type
        message['sender']   = self.identifier

        # Convert to json string
        message = json.dumps(message)

        # Send to the context
        return self.server.send(message, ip, port)

    def inform(self, data: str, address=None) -> str:
        """
        Recives an inform message. Default implementation.
        """

        # Load the data
        message = json.loads(data)

        # Add to the events list
        self.events.append(('message', message['content']))
        
        # Print that the message was recived
        print("Recived: ", message['content'])

        return 'Recived Message'
    
    def tool(self, data: str, address: ...) -> str:
        """
        Request the use of a tool
        """

        # Load data and tool data    
        data = json.loads(data)
        # tool_data = json.loads(data['content'])
    
        # Get the tool and the arguments 
        func = self.tools[data['content']]
        args = data['data']
        
        # Add to the events list
        self.events.append(('message', func, args))

        # Call the tool
        return func(address, *args)
    
    def __repr__(self) -> str:
        return f'<Messenger>'
import json
from threading import Thread
from .messenger import Messenger
from .message import Message
from .server import Server
from .agent import Agent
from .task import Task
import asyncio


class Context(Messenger):
    def __init__(self):
        super().__init__()

        # Agent attributes
        self.agents = {}
        self.available_id = 1
        self.identifier = 0

        # Tasks
        self.task_id = 0
        self.tasks = {}

        # Tools
        self.tools['register']     = self.register
        self.tools['deregister']   = self.deregister
        self.tools['add task']     = self.add_task
        self.tools['get resource'] = self.get_resource
        self.tools['set resource'] = self.set_resource

        # Reasources
        self.resources = {}

        # Create and start the server for reciving messages
        self.server = Server(self.recive)
        
        thread = Thread(target=self.start)
        thread.start()

    def inform(self, data: str, address=None) -> str:
        """
        Send a message out to other agents
        """

        # Load the data
        message = json.loads(data)

        # Send out the message data to all recivers
        for reciver in message['recivers']:
            if reciver == 0:
                print("Recived: ", message['content'])
            elif reciver not in self.agents:
                msg = Message(content=f'Failed to send message to agent {reciver} because they do not exist.')
                self.send(msg, *address)
            else:
                self.server.send(data, *self.agents[reciver])

        # Add to the events list
        self.events.append(('message', message['content']))

        return 'Recived Message'

    def get_resource(self, address: ..., key: str) -> None:
        """
        Gets a context resource and returns it to the requester
        """

        if key not in self.resources:
            self.send(*address, content=f'Failed to get resource {key}', type='inform')
            return

        data = self.resources[key]
        msg = Message(content=f'Got resource {key}: {data}', resources=data, type='inform')
        self.send(msg, *address)

    def set_resource(self, address: ..., key: str, value: ...) -> None:
        """
        Gets a context resource and returns it to the requester
        """

        print(f'Set resource {key} to {value}')

        self.resources[key] = value


    def add_task(self, address: ..., specifications: str, dependencies: list):
        """
        Adds a new task to the context
        """

        # Get the task dependencies from the local tasks dictionary
        deps = []
        for task in dependencies:
            if task not in self.tasks:
                msg = Message(content=f'Failed to add the task. A given task dependency ({task}) does not exist')
                self.send(msg, *address)
                return
            deps.append(self.tasks[task])

        # Make the task and save it with id task_id
        task = Task(specifications, deps)
        self.tasks[self.task_id] = task

        # Increment to maintain unique task ids
        self.task_id += 1

        print(f'Added task: {task}')

    def get_task(self, address: ..., task_id: int):
        """
        Gets a task from the context
        """

        if task_id not in self.tasks:
            msg = Message(content=f'Failed to find task with id {task_id}')
            self.send(msg, *address)
            return
        
        msg = Message(content=f'Failed to find task with id {task_id}')
        self.send(msg, *address)

    def register(self, address: ...) -> int:
        """
        Adds an agent to the context
        """

        print(f'registering agent at {address}')

        # Add to the dict of agents
        self.agents[self.available_id] = address

        # Add to the events list
        self.events.append(('register', (self.available_id, address)))

        # Send the agent its id
        msg = Message(content='register', type='tool', resources=[self.available_id])
        self.send(msg, *address)

        # Increment to maintain unique agent ids
        self.available_id += 1
        
        return str(self.available_id - 1)

    def deregister(self, address, identifier: int):
        """
        Removes an agent from the context
        """

        del self.agents[identifier]

    def __repr__(self) -> str:
        return f'<Context>'
import json
from threading import Thread
from .messenger import Messenger
from .message import Message
from .server import Server, PORT, IP
from .agent import Agent
from .task import Task
import asyncio


class Context(Messenger):
    def __init__(self):
        super().__init__()

        # Agent attributes
        self.agents = {}
        self.available_id = 1

        # Tasks
        self.task_id = 0
        self.tasks = {}

        # Tools
        self.tools['register']        = self.register
        self.tools['deregister']      = self.deregister
        self.tools['get resource']    = self.get_resource
        self.tools['set resource']    = self.set_resource
        self.tools['remove resource'] = self.remove_resource
        self.tools['add task']        = self.add_task
        self.tools['get task']        = self.get_task

        # Reasources
        self.resources = {}

        # Create and start the server for reciving messages
        self.server = Server(self.recive)
        
        thread = Thread(target=self.start)
        thread.start()

    def recive(self, data: str, address=None) -> str:
        """
        Recives a data from the server and sends it to the correct function to handle it
        """
        
        data_dict = json.loads(data)
        if data_dict['sender'] not in self.agents and not (data_dict['type'] == 'tool' and data_dict['content'] == 'register'):
            msg = Message(content=f'You are not registered in this context')
            self.send(msg, *address)
            return

        super().recive(data, address)

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
            msg = Message(content=f'Failed to get resource {key}')
            self.send(msg, *address)
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

    def remove_resource(self, address: ..., key: str) -> None:
        """
        Gets a context resource and returns it to the requester
        """

        if key not in self.resources:
            msg = Message(content=f'Failed to find resource {key}')
            self.send(msg, *address)
            return

        print(f'Removing resource {key}')
        del self.resources[key]

    def add_task(self, address: ..., specifications: str, dependencies: list) -> None:
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
        id = self.task_id
        self.tasks[id] = task

        # Increment to maintain unique task ids
        self.task_id += 1

        print(f'Added task: {task}')

        return id

    def _find_task(self, address: ..., task_id: int) -> Task:
        """
        Find the task if it is availible. Send failure if not found
        """
        
        # Convert str to int
        task_id = int(task_id)

        # Search for it, send failure message if not found
        if task_id not in self.tasks:
            msg = Message(content=f'Failed to find task with id {task_id}')
            self.send(msg, *address)
            return None
        
        # Return the task
        return self.tasks[task_id]

    def get_task(self, address: ..., task_id: int) -> None:
        """
        Gets a task from the context
        """

        # Find the task. Halt if no task was found
        task = self._find_task(task_id)
        if not task: return

        # Send message
        msg = Message(content=f'{task.name} | {task_id} : {task.specifications}\nCurrent Input : {task.input}', resources=task.input, type='inform')
        self.send(msg, *address)

    def remove_task(self, address: ..., task_id: int) -> None:
        """
        Removes the given task from the context
        """

        # Find the task. Halt if no task was found
        task = self._find_task(task_id)
        if not task: return
        
        task_id = int(task_id)
        del self.tasks[task_id]

    def set_task_name(self, address: ..., task_id: int, name: str) -> None:
        """
        Removes the given task from the context
        """

        task = self._find_task(task_id)
        if not task: return
        
        task.name = name

    def set_task_specifications(self, address: ..., task_id: int, specifications: str) -> None:
        """
        Removes the given task from the context
        """

        task = self._find_task(task_id)
        if not task: return
        
        task.specifications = specifications

    def set_task_output(self, address: ..., task_id: int, output: ...) -> None:
        """
        Removes the given task from the context
        """

        task = self._find_task(task_id)
        if not task: return 

        task.output = output

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

    def deregister(self, address, identifier: int) -> None:
        """
        Removes an agent from the context
        """

        identifier = int(identifier)
        if identifier not in self.agents:
            msg = Message(content=f'Failed to find agent with id {identifier}')
            self.send(msg, *address)
            return

        print(f'deregistering agent {identifier} at {self.agents[identifier]}')
        del self.agents[identifier]

    def close(self) -> None:
        """
        Closes the server and all running threads
        """

        self.running = False
        self.send(Message(content="Closing"))

    def __repr__(self) -> str:
        return f'<Context>'
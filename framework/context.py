import pickle
from typing import Any, Optional
from .networking.server import Server
from .networking.network_node import NetworkNode, IP, PORT
from .message import Message, Request, Result, Error, Notification
from .task import Task

class Context(Server):
    def __init__(self):
        super().__init__()

        self.agents = set()
        self.resources = {}
        self.tasks: dict[str, Task] = {}

        self.methods = {
            "register" : self.register,
            "deregister" : self.deregister,
            "set resource" : self.set_resource,
            "get resource" : self.get_resource,
            "add task" : self.add_task,
            "set task status" : self.set_task_status,
            "set task output" : self.set_task_output
        }

    def send(self, message: Message, recivers: list[tuple[str, int] | NetworkNode] | tuple[str, int] | NetworkNode=(IP, PORT)):

        message.sender = self.address
        message.recivers = recivers

        super().send(pickle.dumps(message))

    def receive(self, data: bytes, address: tuple[str, int]) -> None:
        """
        Processes a recived message. 
        """

        message: Message = pickle.loads(data)

        for reciver in message.recivers:
            if reciver == self.address: continue
            self.forward(message, reciver)

        if self.address not in message.recivers: return

        # Handle a message addressed to the context
        self.handle_message(message)

    def forward(self, message, reciver) -> None:
        """Forwards a message from the server to the intended reciver"""
        
        super().send(pickle.dumps(message), reciver)

    # Following methods are provided internal methods for context interaction
    
    def register(self, address: tuple) -> dict:
        """Adds an agent to the context"""
        self.agents.add(address)
        return {"registered" : True}
    
    def deregister(self, address: tuple) -> dict:
        """Removes an agent from the context"""
        self.agents.remove(address)
        return {"registered" : False}
    
    def set_resource(self, name: str, value: Any) -> dict:
        """Removes an agent from the context"""
        self.resources[name] = value
        return {"name" : name, "value" : value}
    
    def get_resource(self, name: str) -> dict | Error:
        """Removes an agent from the context"""
        if name not in self.resources:
            return Error(1, f"Given resource key, {name}, is not in the context.")
        return {"name" : name, "value" : self.resources[name]}
    
    def add_task(self, name: str, specifications: str, dependencies: Optional[list[str]]=None) -> dict | Error:
        """Adds a new task to the context"""

        dependencies_as_tasks = []
        dependencies = dependencies if dependencies else []

        for dependency in dependencies:
            if dependency not in self.tasks:
                return Error(2, f"Got a task dependency that does not exist, {dependency}")
            dependencies_as_tasks.append(self.tasks[dependency])

        self.tasks[name] = Task(name, specifications, dependencies_as_tasks)

        return {"name" : name}
    
    def set_task_status(self, name: str, status: str) -> dict | Error:
        """Sets the status of the tasks. Returns an error if invalid task name or status is given"""

        if name not in self.tasks:
            return Error(3, f"Got a task name that does not exist, {name}")
        if not self.tasks[name].set_status(status):
            return Error(4, f"Invalid task status type, {status}")
        
        return {"name" : name, "status" : status}
    
    def set_task_output(self, name: str, output: Any) -> dict | Error:
        """Sets the status of the tasks. Returns an error if invalid task name is given"""

        if name not in self.tasks:
            return Error(3, f"Got a task name that does not exist, {name}")

        self.tasks[name].output = output
        return {"name" : name, "output" : output}

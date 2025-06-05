import pickle
from typing import Any
from .networking.server import Server
from .message import Message, Result, Error
from .task import Task

class Context(Server):
    """
    Central hub for all node comomunication. 
    All messages pass through the context.
    Contains the registered agents, resources, and tasks.
    """

    agents: set[tuple[str, int]]
    resources: dict[str, Any]
    tasks: dict[str, Task]
    error_log: dict[int, int]

    def __init__(self) -> None:
        """Starts the server and exposes all provided methods. """
        super().__init__()

        # Initialize state attributes
        self.agents = set()
        self.resources = {}
        self.tasks = {}

        # Expose the internally provided methods/tools
        self.methods = {
            "register" : self.register,
            "deregister" : self.deregister,
            "message" : self.message,
            "set resource" : self.set_resource,
            "get resource" : self.get_resource,
            "add task" : self.add_task,
            "set task status" : self.set_task_status,
            "set task output" : self.set_task_output,
            "get task" : self.get_task,
            "get agents" : self.get_registered_agents
        }

        self.error_log = {}

    def receive(self, data: bytes, address: tuple[str, int] | None = None) -> None:
        """
        Processes recived data as a message.
        Forwards messages to recivers other than self and handles messages addressed to the Context.
        Args:
            data (bytes): The byte data of the recived message
            address (tuple[str, int]): Not used, but potentially could be in overrides.
        """

        # Load the data into a message
        message: Message = pickle.loads(data)

        # Log any errors
        if isinstance(message, Error):
            code = message.code
            if code not in self.error_log: self.error_log[code] = 0
            self.error_log[code] += 1

        # Forward the message to all receivers except self
        for receiver in message.receivers:
            if receiver == self.address: continue
            self.forward(message, receiver)

        # Handle a message addressed to the context
        if self.address not in message.receivers: return
        self.handle_message(message)

    def forward(self, message: Message, receiver: tuple[str, int]) -> None:
        """Forwards a message from the server to the intended receiver. """
        self.send_bytes(pickle.dumps(message), receiver)


    # ------------------------- Internal Methods -------------------------

    def register(self, address: tuple) -> Result:
        """Adds an agent to the context"""
        self.agents.add(address)
        return Result("registered", True)
    
    def deregister(self, address: tuple) -> Result:
        """Removes an agent from the context"""
        self.agents.remove(address)
        return Result("registered", False)
    
    def message(self, content: str) -> Result:
        """Receives a message"""
        print("Context received message: ", content)
        return Result("received", True)

    def set_resource(self, name: str, value: Any) -> Result:
        """Sets a resource value. Adds the resource if it does not exist."""
        self.resources[name] = value
        return Result(name, value)
    
    def get_resource(self, name: str) -> Result | Error:
        """Gets a resource value. Returns an error if it does not exist."""
        if name not in self.resources:
            return Error(1, f"Given resource key, {name}, is not in the context.")
        return Result(name, self.resources[name])
    
    def add_task(self, name: str, specifications: str, dependencies: list[str] | None = None) -> Result | Error:
        """Adds a new task to the context"""

        dependencies_as_tasks = []
        dependencies = dependencies if dependencies else []

        for dependency in dependencies:
            if dependency not in self.tasks:
                return Error(2, f"Got a task dependency that does not exist, {dependency}")
            dependencies_as_tasks.append(self.tasks[dependency])

        self.tasks[name] = Task(name, specifications, dependencies_as_tasks)
        return Result("task_name", name)
    
    def set_task_status(self, name: str, status: str) -> Result | Error:
        """Sets the status of the tasks. Returns an error if invalid task name or status is given"""

        if name not in self.tasks:
            return Error(3, f"Got a task name that does not exist, {name}")
        if not self.tasks[name].set_status(status):
            return Error(4, f"Invalid task status type, {status}")
        
        return Result("status", status)
    
    def set_task_output(self, name: str, output: Any) -> Result | Error:
        """Sets the output of the tasks. Returns an error if invalid task name is given"""

        if name not in self.tasks:
            return Error(3, f"Got a task name that does not exist, {name}")

        self.tasks[name].output = output
        return Result("output", output)

    def get_task(self, name) -> Result | Error:
        """Gets the values of a task. Returns an error if invalid task name is given"""
    
        if name not in self.tasks:
            return Error(3, f"Got a task name that does not exist, {name}")
        
        task = self.tasks[name]
        return Result("task", task)
    
    def get_registered_agents(self) -> Result:
        """Gets all the agents currently registered in the context"""
        return Result("agents", self.agents)
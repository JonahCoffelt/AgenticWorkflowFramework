import pickle
from typing import Optional, Any
from .networking.client import Client
from .networking.network_node import IP, PORT
from .message import Notification


class Task():
    name: str
    """Name of the tasks. Useful for identification by human agents"""
    specifications: str
    """A peice of work to be completed"""
    dependencies: list
    """List of tasks that this task is dependent on"""
    status: str
    """Current state of the task (idle, in progress, complete, failed)"""
    output: Optional[Any]
    """Result of the task"""

    def __init__(self, name: str, specifications: str, dependencies: Optional[list]=None):

        # Initialization values
        self.name = name
        self.specifications = specifications
        self.dependencies = dependencies if dependencies else []

        # Default values
        self.status = "idle"
        self.output = None
        self.agents = set()

    def set_status(self, status: str) -> bool:
        """Sets the status of the task. Returns True if a valid status type was given"""
        
        if status not in ("idle", "in progress", "complete", "failed"):
            return False
        
        self.status = status
        return True

    def update(self) -> bool:
        """Checks if the status can be updated. Returns true if status changed"""

        if self.status == "idle" and all(task.status == "complete" for task in self.dependencies):
            self.status = "in progress"
            return True
        
        return False
    
    @property
    def inputs(self) -> list[Any]:
        return [task.output for task in self.dependencies]
    
    def __repr__(self) -> str:
        return f'<Task | {self.specifications}>'
    

class UserTask(Client):
    def __init__(self, name: str, specifications: str, dependencies: Optional[list]=None):
        super().__init__()

        self.name = name
        self.specifications = specifications
        self.dependencies = dependencies if dependencies else []

        for i, dependency in enumerate(self.dependencies):
            if isinstance(dependency, str): continue
            self.dependencies[i] = dependency.name

        # Default values
        self.status = "idle"
        self.output = None
        self.agents = set()

        # Add on the context
        self.send(Notification("add task", {"name" : self.name, "specifications" : self.specifications, "dependencies" : self.dependencies}))

    def send(self, message: Notification):

        message.sender = self.address
        message.recivers = [(IP, PORT)]

        super().send(pickle.dumps(message))
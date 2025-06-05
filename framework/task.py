import pickle
from typing import Optional, Any
from .networking.client import Client
from .message import Request, Error, Notification
from .data_validation import validate_string


class Task():
    """"""

    name: str
    specifications: str
    dependencies: list
    status: str
    output: Optional[Any]

    def __init__(self, name: str, specifications: str, dependencies: Optional[list]=None):
        """
        
        """
        
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

        self.dependencies = dependencies if dependencies else []
        for i, dependency in enumerate(self.dependencies):
            if isinstance(dependency, str): continue
            self.dependencies[i] = dependency.name

        # Add on the context
        self.send(Notification("add task", name=name, specifications=specifications, dependencies=self.dependencies))

        self.name = name
        self.specifications = specifications

        # Default values
        self.status = "idle"
        self.output = None
        self.agents = set()

    def sync(self) -> None:
        """Syncs data with the context. Pauses operation until data is recived"""
        result = self.send(Request("get task", name=self.name))
        task: Task = result.value

        self._specifications = task.specifications
        self._status = task.status
        self._output = task.output
        self._agents = task.agents

    @property
    def name(self) -> str: return self._name
    @property
    def specifications(self) -> str: return self._specifications
    @property
    def dependencies(self) -> str: return self._dependencies
    @property
    def status(self) -> str:
        self.sync()
        return self._status
    @property
    def output(self) -> str: 
        self.sync()
        return self._output

    @name.setter
    def name(self, value: str):
        self._name = validate_string(value)
    @specifications.setter
    def specifications(self, value: str):
        self._specifications = validate_string(value)
    @dependencies.setter
    def dependencies(self, value: str):
        self._dependencies = value
    @status.setter
    def status(self, value: str):
        result = self.send(Request("set task status", name=self.name, status=value))
        if not isinstance(result, Error): self._status = result.value
    @output.setter
    def output(self, value: str):        
        result = self.send(Request("set task output", name=self.name, output=value))
        if not isinstance(result, Error): self._output = result.value
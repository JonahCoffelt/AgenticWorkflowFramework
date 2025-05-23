from typing import Any
from .message import Message


class Task:
    name: str
    """Name of the tasks. Useful for identification by human agents"""
    specifications: str
    """A peice of work to be completed"""
    dependencies: list
    """List of tasks that this task is dependent on"""
    status: int
    """Current state of the task (idle, in progress, complete, failed)"""
    output: ...
    """Result of the task"""

    def __init__(self, specifications: str, dependencies: list):
        """
        
        """
        
        self.name = 'Task'
        self.specifications = specifications
        self.dependencies   = dependencies
        self.status = 0
        self.output = None
        self.agents = set()

    def update(self) -> None:
        """
        
        """
        if self.status == 0 and all(task.status == 2 for task in self.dependencies):
            self.status = 1
            return Message(content=f'{self.name} : Task status has been marked updated to in progress, you can now start.', resources=self.input, type='inform')

    @property
    def input(self) -> list[Any]:
        return [task.output for task in self.dependencies]

    def __repr__(self) -> str:
        return f'<Task | {self.specifications}>'
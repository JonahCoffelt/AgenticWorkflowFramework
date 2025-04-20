from typing import Any


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

    @property
    def input(self) -> list[Any]:
        return [task.output for task in self.dependencies]

    def __repr__(self) -> str:
        return f'<Task | {self.specifications}>'
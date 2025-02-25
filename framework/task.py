from typing import Any
from .flags import *
from .agent import Agent

class Task:
    specification: Any
    """Specifications for what the task should do"""

    status: int=10
    """Flag for determining the current state of the tasks. Allows for task dependency"""
    agent: Agent=None
    """The agent that the task is assigned to. Assuming one agent per task"""
    input: Any=0
    """Input being passed in from other tasks or the eviornment"""
    output: Any=0
    """The resulting output from the task"""

    dependencies: list
    """"""

    def __init__(self, specification, *dependencies):
        """
        
        """

        self.specification = specification
        self.dependencies = list(dependencies)

        self.status = STATUS_IDLE

        self.input  = 0
        self.output = 0

    def update(self):
        """
        Update loop for the task
        """

        match self.status:
            case int(STATUS_IDLE):
                pass
            case int(STATUS_IN_PROGRESS):
                pass
            case int(STATUS_FAILED):
                pass
            case int(STATUS_COMPLETE):
                pass
            case _:
                pass

    @property
    def degree(self) -> int:
        return len(self.dependencies)

    def __repr__(self) -> str:
        return str(self.specification)
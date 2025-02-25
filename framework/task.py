from typing import Any
from .flags import *
from .agent import Agent

class Task:
    def __init__(self, specification, *dependencies) -> None:
        """
        
        """

        self.specification = specification
        self.dependencies = list(dependencies)

        self.status = STATUS_IDLE

        self.input  = 0
        self.output = 0

    def update(self) -> None:
        """
        TODO: Update loop for the task
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
        """The number of dependencies the task has"""
        return len(self.dependencies)

    def __repr__(self) -> str:
        return str(self.specification)
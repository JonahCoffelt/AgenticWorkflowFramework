from typing import Any
from .flags import *
from .agent import Agent
import asyncio

class Task:
    output: list[Any]
    """"""
    status: int
    """"""
    
    
    def __init__(self, func, *dependencies) -> None:
        """
        
        """

        self.func = func
        self.dependencies = list(dependencies)

        self.status = STATUS_IDLE

        self.output = []

    async def update(self) -> None:
        """
        TODO: Update loop for the task
        """

        if self.status == STATUS_IDLE and all([dep.status == STATUS_COMPLETE for dep in self.dependencies]):
            self.status = STATUS_IN_PROGRESS

        if self.status == STATUS_IN_PROGRESS:
            args = []
            for dep in self.dependencies: args.extend(dep.output)

            try: 
                out = await self.func(*args)
                self.output.extend([out])
                self.status = STATUS_COMPLETE
            except:
                print("Task failed")
                self.status = STATUS_FAILED


    @property
    def degree(self) -> int:
        """The number of dependencies the task has"""
        return len(self.dependencies)

    def __repr__(self) -> str:
        return f'<Task | {self.func}>'
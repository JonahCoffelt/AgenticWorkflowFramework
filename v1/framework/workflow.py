import asyncio
from .task import Task
from .flags import *
from math import sqrt


class Workflow:
    tasks: set[Task]
    """Set containing all tasks in the workflow"""
    ordering: list[set[Task]]
    """The general ordering of the tasks assuming uniform time completion"""
    def __init__(self, *tasks: Task) -> None:
        """
        A container for a sequence of tasks
        """
        
        self.tasks = set(task for task in tasks)
        self.build_graph()
        self.build_task_ordering()
        self.initialize_tasks()

    def build_graph(self) -> None:
        """
        Builds a graph based on the given tasks and their dependencies
        """
        
        # Add all the tasks to the top level of the graph
        self.graph = {task : set() for task in self.tasks}

        # Add all connections based on task dependencies
        for task in self.tasks:
            for dependency in task.dependencies:
                self.graph[task].add(dependency)

    def build_task_ordering(self) -> None:
        """
        Builds na ordering of the tasks that may be completed at any given stage of the workflow.
        This does not prescribe the order that tasks mist be completed in.
        The ordering allows for analysis of parallelism
        """

        # Initalize ordering with base case step
        self.ordering = [set()]
        visited_tasks = set()

        # Loop through until all tasks are in the ordering
        while len(visited_tasks) != len(self.tasks):
            # Get the tasks that can be completed next
            new_tasks = set(filter(lambda task: all([dep in visited_tasks for dep in task.dependencies]), self.tasks)).difference(visited_tasks)

            # # Drag along tasks that are a direct dependency down the line
            # required_tasks = new_tasks.union(filter(lambda task: any([task in other.dependencies for other in self.tasks.difference(visited_tasks.union(new_tasks))]), self.ordering[-1]))

            # Add the new tasks and step
            self.ordering.append(new_tasks)
            visited_tasks.update(new_tasks)

        # Dont care about the base case step
        self.ordering = self.ordering[1:]

    def initialize_tasks(self):
        """
        Starts all tasks at the start of the graph
        """

        for task in self.ordering[0]:
            task.status = STATUS_IN_PROGRESS

    async def update(self) -> None:
        """
        TODO: Will update the tasks and make them do things
        """

        task_functions = []
        for task in self.tasks:
            task_functions.append(asyncio.create_task(task.update()))

        for task in task_functions:
            await task

    def start(self) -> None:
        while any([task.status != STATUS_COMPLETE and task.status != STATUS_FAILED for task in self.tasks]):
            asyncio.run(self.update())

    @property
    def parallelism(self) -> int:
        """Gets the parallelism of the workflow, a measure of how well tasks can be concurently completed throughout the workflow"""
        return sum([len(step) / len(self.tasks) for step in self.ordering]) / len(self.ordering)
    
    @property
    def complexity(self) -> int:
        """Gets the dependency complexity of the workflow, a measure of the complexity of the workflow structure """
        d_mean = sum([task.degree for task in self.tasks]) / len(self.tasks)
        return sqrt(sum([(task.degree - d_mean) ** 2 for task in self.tasks]) / len(self.tasks))
    
    def __repr__(self):
        return f'<Workflow | {self.ordering}>'
        
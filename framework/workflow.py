from .task import Task
from math import sqrt

class Workflow:
    def __init__(self, *tasks: Task):
        """
        A container for a sequence of tasks
        """
        
        self.tasks = set(task for task in tasks)
        self.build_graph()
        self.build_task_ordering()

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

            # Drag along tasks that are a direct dependency down the line
            required_tasks = new_tasks.union(filter(lambda task: any([task in other.dependencies for other in self.tasks.difference(visited_tasks.union(new_tasks))]), self.ordering[-1]))

            # Add the new tasks and step
            self.ordering.append(required_tasks)
            visited_tasks.update(new_tasks)

        # Dont care about the base case step
        self.ordering = self.ordering[1:]

    def update(self):
        """
        TODO: Will update the tasks and make them do things
        """

    @property
    def parallelism(self) -> int:
        return sum([len(step) / len(self.tasks) for step in self.ordering]) / len(self.ordering)
    
    @property
    def complexity(self) -> int:
        d_mean = sum([task.degree for task in self.tasks]) / len(self.tasks)
        return sqrt(sum([(task.degree - d_mean) ** 2 for task in self.tasks]) / len(self.tasks))
        
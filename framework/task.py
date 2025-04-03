

class Task:
    
    specifications: str
    """A peice of work to be completed"""
    dependencies: list
    """List of tasks that this task is dependent on"""
    status: int
    """Current state of the task (idle, in progress, complete, failed)"""
    output: ...
    """Result of the task"""

    def __init__(self, specifications: str, dependencies: list):
        self.specifications = specifications
        self.dependencies   = dependencies
        self.status = 0
        self.output = None

    def __repr__(self):
        return f'<Task | {self.specifications}>'
from .node import Node


class NodeHandler:
    nodes: list[Node]
    """List of all the nodes in the dashboard"""
    
    def __init__(self):
        self.nodes = []


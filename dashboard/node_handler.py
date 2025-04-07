from .node import Node


class NodeHandler:
    nodes: list[Node]
    """List of all the nodes in the dashboard"""
    
    def __init__(self, ui):
        self.ui = ui
        self.nodes = [Node(self) for i in range(10)]
        self.nodes.append(Node(self))

    def draw(self):
        """
        Draws all nodes in the context
        """
        
        for node in self.nodes:
            node.draw()

    def collide(self, x, y) -> Node | None:
        """
        Checks if the position collides with any nodes.
        Returns the collided node or None
        """
        
        x, y = self.ui.grid.screen_to_world((x, y))

        for node in self.nodes:
            if node.collide(x, y): return node
        
        return None
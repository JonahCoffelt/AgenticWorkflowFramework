from .node import Node


class Client(Node):
    """Wrapper class for NetworkNode that does not specify the port."""
    def __init__(self):
        super().__init__(port=0)
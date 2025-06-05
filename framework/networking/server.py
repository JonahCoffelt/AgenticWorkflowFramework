from .node import Node


class Server(Node):
    """Wrapper class for NetworkNode on the internally defined port."""
    def __init__(self):
        super().__init__()
from .context_node import ContextNode


class Server(ContextNode):
    def __init__(self):
        """Wrapper class for NetworkNode on the internally defined port"""
        super().__init__()
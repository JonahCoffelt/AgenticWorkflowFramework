from .context_node import ContextNode


class Client(ContextNode):
    def __init__(self):
        """Wrapper class for NetworkNode that does not specify the port"""
        super().__init__(port=0)
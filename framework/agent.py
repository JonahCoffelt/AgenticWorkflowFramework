from .networking.client import Client
from .message import Request, Result
from .data_validation import validate_bool


class Agent(Client):
    """Basic agent on the context."""

    is_registered: bool

    def __init__(self):
        """Starts a client for agent-context communication and registers the agent on the context."""
        super().__init__()
 
        self.methods = {
            'message' : self.message
        }


        # Register with the context
        result: Result = self.send(Request("register", address=self.address))
        self.is_registered = validate_bool(result.value)

    # ------------------------- Exposed Methods/Tools -------------------------

    def message(self, content: str) -> Result:
        """Receives a message"""
        print("Context received message: ", content)
        return Result("received", True)
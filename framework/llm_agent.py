from .agent import Agent
from .llm import LLM
from .llm_tools import LLMTools
from .message import Message, Result, Request, Notification, Error

class LLMAgent(Agent):
    """"""
    
    def __init__(self):
        """"""
        super().__init__()

        self.methods = {
            'message' : self.message
        }

        self.tools = LLMTools(self)
        self.llm = LLM(tools_map=self.tools.tools_map, tools_definition=self.tools.tools_definition)

    def call_method(self, message: Request | Notification, address: tuple[str, int]=None) -> Result | Error | None:
        """Calls a method from a request or notification. Returns the result."""
        # Get data from the message
        method = message.method
        params = message.params

        # Verify valid method request
        if method not in self.methods:
            return Error(5, f"Got invalid method identifier: {method}")
        
        # Call the method and return result
        try:
            result = self.methods[method](**params, address=address)
            return result
        except TypeError:
            return Error(6, f"Got invalid method parameters for {method}: {params}")


    # ------------------------- Exposed Methods/Tools -------------------------

    def message(self, content: str, address: tuple[int, str]) -> Result:
        """Receives a message and gets a response from the llm."""

        # Temporary debug print
        print(f"LLM received message from {address}: ", content)

        # Add the sender address to the message so the AI can send back
        content = f"From {address}: " + content

        # Add the message to the history and get a response
        self.llm.add_message(content)
        response = self.llm.get_response()
        return Result("response", response)

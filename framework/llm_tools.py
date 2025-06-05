from pydantic import BaseModel, Field
from typing import List, Tuple
from .agent import Agent
from .message import Notification


class SendMessage(BaseModel):
    content: str = Field(..., description="The content of the message to send.")
    # Define receivers as a list where each item is a tuple of (string, integer)
    receivers: List[Tuple[str, int]] = Field(
        ...,
        description="A list of recipient addresses, where each address is a tuple containing the IP address (string) and the port number (integer). Example: [('127.0.0.1', 5051), ('192.168.1.10', 8080)]"
    )

send_message_schema = SendMessage.model_json_schema()


class LLMTools:
    """"""
    
    agent: Agent
    tools_map: dict[str, callable]
    tools_definition: list[dict]
    
    def __init__(self, agent: Agent):
        """
        Handles tool definitions and tools maps for LLM agents

        Args:
            agent (Agent): Reference to the agent that uses this class 
        """
        
        self.agent = agent

        self.tools_map = {
            
        }

        self.tools_definition = [
            
        ]

    def send_message(self, content: str, receivers: List[Tuple[str, int]]) -> None:

        print("LLM sending ", content, " to ", receivers)
        for i, receiver in enumerate(receivers):
            if isinstance(tuple): continue
            else: receivers[i] = tuple(receiver)

        notif = Notification("messagae", content=content)
        self.agent.send(notif, receivers)
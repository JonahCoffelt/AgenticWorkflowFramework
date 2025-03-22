import json


class Agent:
    identifier: int
    """Unique global identifier for the agent"""
    role: str
    """The role the agent plays in the context. Serves as a permision level"""
    type: str
    """Either AI or human"""

    def __init__(self):
        ...

    def message(self, message: str):
        """
        Sends a message to this agent
        """

        message = json.loads(message)
        print(message)

    def __repr__(self) -> str:
        return f'<Agent | id: {self.identifier}>'
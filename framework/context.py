from .agent import Agent
import json

class Context:
    def __init__(self):
        """
        Defines the enviornment in which agents interact
        """
        
        # Agent attributes
        self.agents = {}
        self.available_id = 0

    def send(self, message: str):
        """
        Send a message to interact with the context
        """

        message = json.loads(message)


        for reciver in message['recivers']:
            agent = self.agents[reciver]
            agent.message(json.dumps(message))

    def register(self, agent: Agent):
        """
        Adds an agent to the context
        """

        # Set to a unique identifier in this context
        agent.identifier = self.available_id
        self.available_id += 1

        # Add to the dict of agents
        self.agents[agent.identifier] = agent

    def deregister(self, agent: Agent):
        """
        Removes an agent from the context
        """

        del self.agents[agent.identifier]
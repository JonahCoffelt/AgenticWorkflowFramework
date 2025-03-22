from .flags import *

class Agent:
    def __init__(self, type: int=AGENT_TYPE_HUMAN) -> None:
        self.type = AGENT_TYPE_HUMAN
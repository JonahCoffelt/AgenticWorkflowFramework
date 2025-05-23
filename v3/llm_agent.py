import json
import time
from .agent import Agent
from .message import Message
from .llm import LLM
from .llm_tool_schemas import MessageRequest, SetTaskOutputRequest, SetTaskStatusRequest, message_request_schema, set_task_output_request_schema, set_task_status_request_schema


class LLMAgent(Agent):
    def __init__(self, role_prompt: str, task: int):
        """
        Implementation of an LLM agent
        """
        super().__init__()

        time.sleep(.2)

        self.task_id = task
        self.send(Message(type='tool', content='claim task', resources=[self.identifier, self.task_id]))

        tools_map = {
            "send_message" : self.message,
            "get_task" : self.get_task,
            "set_task_output" : self.set_task_output,
            "set_task_status" : self.set_task_status,
        }

        tools_definition = [
            {
                "type": "function",
                "function": {
                    "name": "send_message",
                    "description": "Sends a message to a given list of recivers.",
                    "parameters": message_request_schema,
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_task",
                    "description": "Get the current task",
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "set_task_output",
                    "description": "Sets the output of the current task. The output should be the data resulting from the task, not a completion message. ",
                    "parameters": set_task_output_request_schema,
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "set_task_status",
                    "description": "Sets the status of the current task. Task status 0 means idle, 1 means in progress, 2 means finished, 3 means failed.",
                    "parameters": set_task_status_request_schema,
                },
            },
        ]

        self.llm = LLM(tools_map=tools_map, tools_definition=tools_definition)

        role_prompt = "You are an AI agent in a multi-agent system. According to the users, your role is: " + role_prompt
        with open('framework/prompt.txt', 'r') as file:
            role_prompt += file.read()
        role_prompt += "Your id is " + str(self.identifier)


        self.llm.message(role_prompt)


    def message(self, **kwargs) -> None:
        """
        Generates and sends a message. This is a simplified wrapper for the AI to use
        """

        # Validate input
        request = MessageRequest(**kwargs)

        print("Agent Sending: \"", request.content, "\" to ", request.recivers)
        self.send(Message(content=request.content, recivers=request.recivers))

    def get_task(self, **kwargs) -> None:
        """
        Gets the AI's task. Wrapper to make task access easier
        """
        
        print("Getting task")

        # Send out request
        self.send(Message(type='tool', content='get task', resources=[self.task_id]))

    def set_task_status(self, **kwargs) -> None:
        """
        Wrapper to make task modification easier
        """


        # Validate input
        request = SetTaskStatusRequest(**kwargs)
        print("Setting task status to ", request.status)

        # Send out request
        self.send(Message(type='tool', content='set task status', resources=[self.task_id, request.status]))

    def set_task_output(self, **kwargs) -> None:
        """
        Wrapper to make task modification easier
        """

        # Validate input
        request = SetTaskOutputRequest(**kwargs)
        print("Setting task output to ", request.data)

        # Send out request
        self.send(Message(type='tool', content='set task output', resources=[self.task_id, request.data]))



    def inform(self, data: str, address=None) -> str:
        """
        Recives an inform message. Default implementation.
        """

        # Load the data
        message = json.loads(data)

        # Add to the events list
        self.events.append(('message', message['content']))

        # Print that the message was recived
        print("Recived: ", message['content'])

        print(self.llm.message(str(message)))

        return 'Recived Message'
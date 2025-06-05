import os
import json
import groq
from groq.types.chat import ChatCompletion

API_KEY = os.getenv("AI_API_KEY")
API_KEY = "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"  # Remove for git commits

class LLM:
    """Class to handle API calls to Groq for accessible LLM integration."""
    
    model: str
    client: groq.Client
    messages: list[dict[str, str]]
    tools_map: dict[str, callable]
    tools_definition: list[dict]
    
    def __init__(self, model: str="llama-3.3-70b-versatile", tools_definition=None, tools_map=None):
        """
        Creates an LLM client with the given model. 
        Accepts a tools definition and tools map. If one is given, both must be.
        """

        # Create the client
        self.model = model
        self.client = groq.Groq(api_key=API_KEY)

        # Verify that both or neither of tools_definition and tools_map is provided
        if (tools_definition is None and tools_map is not None) or (tools_definition is not None and tools_map is None):
            raise ValueError("If either 'tools_definition' or 'tools_map' is provided, both must be.")
        
        # State attributes
        self.tools_definition = tools_definition
        self.tools_map = tools_map or {}
        self.messages = []

    def add_message(self, message: str, role: str="user") -> str:
        """
        Adds a new message from the given role to the message history.
        Role defaults to user.
        
        Args:
            message (str): The content of the message.
            role (str): The role of the sender (e.g., 'user', 'system', 'assistant', 'tool').
        """

        self.messages.append({"role": role, "content": message})

    def get_response(self) -> str:
        """
        Gets the llm response given the current message history.
        Calls any needed tools.
        """

        # Get the initial response
        response = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            tools=self.tools_definition, 
            tool_choice="auto",
        )

        # Add the message to message history
        msg = response.choices[0].message
        message_to_append = {
            "role": msg.role,
            "content": msg.content,
        }

        # Handle tool calls specifically
        if msg.tool_calls:
            message_to_append["tool_calls"] = [tool_call.model_dump() for tool_call in msg.tool_calls]
            message_to_append["content"] = None 
            if msg.function_call is not None:
                message_to_append["function_call"] = msg.function_call.model_dump()

        self.messages.append(message_to_append)

        # Check if any tools are used
        if response.choices[0].message.tool_calls:
            self.call_tools(response)
        
        return response.choices[0].message.content

    def call_tools(self, response: ChatCompletion) -> None:
        """
        Calls all tools used in an llm response. 
        Saves the results to the message history.
        """

        for tool_call in response.choices[0].message.tool_calls:

            # Get the tool function name and arguments Grok wants to call
            function_name = tool_call.function.name
            if function_name not in self.tools_map:
                self.messages.append({
                        "role": "tool",
                        "content": json.dumps({"error": f"Function {function_name} not found"}),
                        "tool_call_id": tool_call.id
                    })
                continue
            function_args = json.loads(tool_call.function.arguments)

            # Call one of the tool function defined earlier with arguments
            result = self.tools_map[function_name](**function_args)

            # Append the result from tool function call to the chat message history,
            self.messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id
                }
            )
    

if __name__ == '__main__':
    llm = LLM()

    user_message = input("Enter your message: ")
    while user_message:
        llm.add_message(user_message)
        print(llm.get_response())
        user_message = input("Enter your message: ")
import os
import json
import time
from groq import Groq


API_KEY = os.getenv("AI_API_KEY")

class LLM:
    def __init__(self, model: str="llama-3.3-70b-versatile", tools_definition=None, tools_map=None):
        """
        Wrapper for llm api calls to the given model
        Maintains message history and tools.
        """

        self.model = model
        self.client = Groq(api_key=API_KEY)

        self.tools_definition = tools_definition
        self.tools_map = tools_map

        self.messages = []

    def message(self, message: str) -> str:
        """Gets the llm response given a list of previous messages and a new message"""

        self.messages.append({"role": "user", "content": message})
        return self.respond()

    def respond(self) -> str:
        """Gets the llm response given a list of previous messages"""

        # Get the initial response
        got_valid_reponse = False
        while not got_valid_reponse:
            try:
                response = self.client.chat.completions.create(
                    messages=self.messages,
                    model=self.model,
                    tools=self.tools_definition, 
                    tool_choice="auto",
                )
                got_valid_reponse = True
            except:
                print("Failed to get valid LLM response, trying again...")


        # Add the message to message history
        msg = response.choices[0].message
        self.messages.append(msg)

        # Check if any tools are used
        if response.choices[0].message.tool_calls:
            return self.call_tools(response)
        
        return response.choices[0].message.content

    def call_tools(self, response: ...) -> str:
        """Calls all tools used in an llm response"""

        for tool_call in response.choices[0].message.tool_calls:

            # Get the tool function name and arguments Grok wants to call
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Call one of the tool function defined earlier with arguments
            result = self.tools_map[function_name](**function_args)

            # Append the result from tool function call to the chat message history,
            # with "role": "tool"
            self.messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id  # tool_call.id supplied in Grok's response
                }
            )

        return "Used tools"
    

if __name__ == '__main__':
    llm = LLM()

    user_message = input("Enter your message: ")
    while user_message:
        print(llm.message(user_message))
        user_message = input("Enter your message: ")
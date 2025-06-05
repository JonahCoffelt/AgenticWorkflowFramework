import framework as fmk

ctx = fmk.Context()
llm = fmk.LLMAgent()
user = fmk.Agent()


while True:
    msg = input("Enter a message: ")
    print(user.call_tool("message", receiver=llm.address, content=msg).value)
import framework as fmk

agent = fmk.Agent()

while True:
    msg = input("Enter a message: ")
    agents = list(agent.call_tool("get agents").value)
    agent.call_tool("message", receivers=agent.address, content=msg)
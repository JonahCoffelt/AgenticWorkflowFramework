import framework as fmk
import random
import time

def add(x: int, y: int) -> fmk.Result:
    return fmk.Result("sum", x + y)

ctx = fmk.Context()
agent1 = fmk.Agent()
agent2 = fmk.Agent()

ctx.add_tool("add", add)

x = fmk.Resource("x", 2)
y = fmk.Resource("y", 6)

task1 = fmk.Task("task1", "This is a thing to do")
task2 = fmk.Task("task2", "This is another thing to do", [task1])
task1.output = 4
task1.status = "complete"

tool_result = agent2.call_tool("add", x=2, y=56)
print(tool_result.value)
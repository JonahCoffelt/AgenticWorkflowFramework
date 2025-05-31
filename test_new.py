import framework as fmk
import time

def add(x: int, y: int) -> fmk.Result:
    return fmk.Result("sum", x + y)

ctx = fmk.Context()
agent1 = fmk.Agent()
agent2 = fmk.Agent()

agent1.add_tool("add", add)

x = fmk.Resource("x", 2)
y = fmk.Resource("y", 6)

task1 = fmk.Task("task1", "This is a thing to do")
task2 = fmk.Task("task2", "This is another thing to do", [task1])
task1.output = 4
task1.status = "complete"
task1.status = "complete2"

print(x.value)
print(ctx.error_log)
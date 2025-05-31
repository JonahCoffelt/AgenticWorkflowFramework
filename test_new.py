import framework as fmk
import time

ctx = fmk.Context()
agent1 = fmk.Agent()
agent2 = fmk.Agent()

x = fmk.Resource("x", 2)
y = fmk.Resource("y", 6)
x.value = 3

task1 = fmk.Task("task1", "This is a thing to do")
task2 = fmk.Task("task2", "This is another thing to do", [task1])
task1.output = 6
task1.status = "complete"
task1.send(fmk.Notification("set resource", name="x", value=56))

print(x.value)
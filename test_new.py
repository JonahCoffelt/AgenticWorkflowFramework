import framework as fmk
import time

ctx = fmk.Context()
agent1 = fmk.Agent()
agent2 = fmk.Agent()

x = fmk.Resource("x", 2)
y = fmk.Resource("y", 6)

x.value = 3
print(x.value)

task1 = fmk.Task("task1", "This is a thing to do")
task2 = fmk.Task("task2", "This is another thing to do", [task1])
agent1.send(fmk.Notification("set task output", {"name" : "task1", "output" : 5}))
agent1.send(fmk.Notification("set task status", {"name" : "task1", "status" : "complete"}))

time.sleep(.2)

print(ctx.tasks)
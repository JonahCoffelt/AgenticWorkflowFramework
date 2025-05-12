import framework as fmk
import time
from threading import Thread

ctx = fmk.Context()
# Sample workflow
ctx.add_task((0, 0), "Set the output to 2 (as an int)", [])

ctx.add_task((0, 0), "Set the output to the input (as an int) multiplied 3", [0])
ctx.add_task((0, 0), "Set the output to the input (as an int) multiplied 4", [0])

ctx.add_task((0, 0), "Set the output to the sum of the two inputs (as an int)", [1, 2])

for i in range(4):
    Thread(target=lambda task :fmk.LLMAgent("Do tasks. ", task), args=[i]).start()
    
time.sleep(2)

# Set the first task to in progress
print("Starting Workflow")
ctx.set_task_status((0, 0), 0, 1)
ctx.send_message(fmk.Message("Start your task", recivers=[1]))


while True:
    time.sleep(10)
    print("ping")
    ctx.send_message(fmk.Message("If your task is availible (status already 1), do it. If it is done, do not change it, just send a confirmation message to me.", recivers=[1, 2, 3, 4]))
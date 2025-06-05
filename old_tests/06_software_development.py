import framework as fmk
import time
from threading import Thread

ctx = fmk.Context()
# Sample workflow
ctx.add_task((0, 0), "Create a function in python that adds two numbers. set it to the output of the task", [])
ctx.add_task((0, 0), "The function you are given in python is supposed to subtract two numbers. Please make any corrections needed. ", [0])


time.sleep(1)


for i in range(2):
    Thread(target=lambda task :fmk.LLMAgent("Write or edit code. ", task), args=[i]).start()
    time.sleep(1)
    
time.sleep(1)

# Set the first task to in progress
print("Starting Workflow")
# ctx.set_task_status((0, 0), 0, 1)
ctx.send_message(fmk.Message("Start your task", recivers=[1]))

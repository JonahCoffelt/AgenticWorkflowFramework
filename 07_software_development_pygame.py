import framework as fmk
import time
from threading import Thread

ctx = fmk.Context()
# Sample workflow
ctx.add_task((0, 0), "Create a program in python that makes a pygame window with a simple update loop. Dont include task info in the code. ", [])
ctx.add_task((0, 0), "Given the pygame program, add a red square to the screen. Dont include task info in the code. ", [0])
ctx.add_task((0, 0), "Given the pygame program, add a blue controllable player. Dont include task info in the code. ", [1])
ctx.add_task((0, 0), "Given the pygame program, make an corrections needed. Dont include task info in the code. ", [2])
ctx.set_task_status((0, 0), 0, 1)

time.sleep(1)

for i in range(4):
    Thread(target=lambda task :fmk.LLMAgent("Write or edit code. ", task), args=[i]).start()
    
time.sleep(1)

# Set the first task to in progress
print("Starting Workflow")
ctx.send_message(fmk.Message("Start your task", recivers=[1]))
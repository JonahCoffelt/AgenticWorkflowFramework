import framework as fmk

ctx = fmk.Context()

# Sample workflow
ctx.add_task((0, 0), "Set the output to 2 (as an int)", [])

ctx.add_task((0, 0), "Set the output to the input (as an int) multiplied 3", [0])
ctx.add_task((0, 0), "Set the output to the input (as an int) multiplied 4", [0])

ctx.add_task((0, 0), "Set the output to the sum of the two inputs (as an int)", [1, 2])

# Set the first task to in progress
ctx.set_task_status((0, 0), 0, 1)
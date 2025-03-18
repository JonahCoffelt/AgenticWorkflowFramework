import framework as fmk
from sample_tasks import add_input, multiply_input, display_output

task_1 = fmk.Task(add_input)
task_2 = fmk.Task(multiply_input, task_1)
task_3 = fmk.Task(display_output, task_2)

workflow = fmk.Workflow(task_1, task_2, task_3)

workflow.start()
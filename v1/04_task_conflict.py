import framework as fmk
from sample_tasks import get_nums, get_sum, auto_sum, show_readings

task_1 = fmk.Task(get_nums)
task_2 = fmk.Task(get_sum, task_1)
task_3 = fmk.Task(auto_sum, task_1)
task_4 = fmk.Task(show_readings, task_2, task_3)


workflow = fmk.Workflow(task_1, task_2, task_3, task_4)

workflow.start()
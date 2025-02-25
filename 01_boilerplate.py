import framework as fmk

print("---- sequential tasks ----")
task_1 = fmk.Task("Task 1")
task_2 = fmk.Task("Task 2", task_1)
task_3 = fmk.Task("Task 3", task_2)
task_4 = fmk.Task("Task 4", task_3)
task_5 = fmk.Task("Task 5", task_4)

workflow = fmk.Workflow(task_1, task_2, task_3, task_4, task_5)

print(workflow.graph)
print(workflow.ordering)
print(workflow.parallelism)
print(workflow.complexity)

print("---- parallel tasks ----")

task_1 = fmk.Task("Task 1")
task_2 = fmk.Task("Task 2", task_1)
task_3 = fmk.Task("Task 3", task_1)
task_4 = fmk.Task("Task 4", task_2)
task_5 = fmk.Task("Task 5", task_3, task_4)

workflow = fmk.Workflow(task_1, task_2, task_3, task_4, task_5)

print(workflow.graph)
print(workflow.ordering)
print(workflow.parallelism)
print(workflow.complexity)
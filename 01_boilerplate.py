import framework as fmk

print("\n---- sequential tasks ----")
task_1 = fmk.Task("Task 1")
task_2 = fmk.Task("Task 2", task_1)
task_3 = fmk.Task("Task 3", task_2)
task_4 = fmk.Task("Task 4", task_3)
task_5 = fmk.Task("Task 5", task_4)

workflow = fmk.Workflow(task_1, task_2, task_3, task_4, task_5)

print(workflow)
print(f'Parallelism: \t\t{workflow.parallelism}')
print(f'Dependency Complexity: \t{workflow.complexity}')

print("\n---- parallel tasks ----")

task_1 = fmk.Task("Task 1")
task_2 = fmk.Task("Task 2", task_1)
task_3 = fmk.Task("Task 3", task_1)
task_4 = fmk.Task("Task 4", task_2)
task_5 = fmk.Task("Task 5", task_3, task_4)

workflow = fmk.Workflow(task_1, task_2, task_3, task_4, task_5)

print(workflow)
print(f'Parallelism: \t\t{workflow.parallelism}')
print(f'Dependency Complexity: \t{workflow.complexity}')
import basilisk as bsk
import framework as fmk
engine = bsk.Engine(title="Graph Visualization", grab_mouse=False)

task_1 = fmk.Task("Task 1")
task_2 = fmk.Task("Task 2", task_1)
task_3 = fmk.Task("Task 3", task_1)
task_4 = fmk.Task("Task 4", task_2)
task_5 = fmk.Task("Task 5", task_3, task_4)
task_9 = fmk.Task("Task 3", task_1)

workflow = fmk.Workflow(task_1, task_2, task_3, task_4, task_5, task_9)


while engine.running:

    # Keep track of drawn tasks
    visited_tasks = set()
    # Graph display attributes
    n_layers = len(workflow.ordering)
    layer_width = engine.win_size[0] // n_layers

    for layer in range(n_layers):
        tasks = workflow.ordering[layer]
        n_tasks = len(tasks.difference(visited_tasks))
        visited_tasks.update(tasks)

        for task in range(n_tasks):
            bsk.draw.circle(engine, (255, 100, 100), ((layer + .5) * layer_width, 400 - (len(tasks) - task * 2 - 1) * layer_width//2), layer_width//4)

    engine.update()
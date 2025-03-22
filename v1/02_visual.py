import basilisk as bsk
import framework as fmk
engine = bsk.Engine(title="Graph Visualization", grab_mouse=False)

# Linear workflow
task_1 = fmk.Task("Task 1")
task_2 = fmk.Task("Task 2", task_1)
task_3 = fmk.Task("Task 3", task_2)
task_4 = fmk.Task("Task 4", task_3)
task_5 = fmk.Task("Task 5", task_4)
workflow_1 = fmk.Workflow(task_1, task_2, task_3, task_4, task_5)

# Parallel workflow
task_1 = fmk.Task("Task 1")
task_2 = fmk.Task("Task 2", task_1)
task_3 = fmk.Task("Task 3", task_1)
task_4 = fmk.Task("Task 4", task_2)
task_5 = fmk.Task("Task 5", task_3, task_4)
workflow_2 = fmk.Workflow(task_1, task_2, task_3, task_4, task_5)

# Complex workflow
task_1 = fmk.Task("Task 1")
task_2 = fmk.Task("Task 2", task_1)
task_3 = fmk.Task("Task 3", task_1)
task_4 = fmk.Task("Task 4", task_1)
task_5 = fmk.Task("Task 5", task_3, task_4)
task_6 = fmk.Task("Task 6", task_2, task_5)
workflow_3 = fmk.Workflow(task_1, task_2, task_3, task_4, task_5, task_6)

current_workflow = workflow_1

def draw_workflow(workflow: fmk.Workflow) -> None:
    """
    Draws the ordering of a given workflow
    TODO: Add node connections
    """
    
    # Keep track of drawn tasks
    visited_tasks = set()

    # Graph display attributes
    n_layers = len(workflow.ordering)
    layer_width = engine.win_size[0] // n_layers if n_layers else 0

    for layer in range(n_layers):
        tasks = workflow.ordering[layer]
        n_tasks = len(tasks.difference(visited_tasks))
        visited_tasks.update(tasks)

        for task in range(n_tasks):
            h = 400 - len(tasks) * layer_width // 2 + (task + .5) * layer_width
            bsk.draw.circle(engine, (255, 100, 100), ((layer + .5) * layer_width, h), layer_width//4)

def select_workflow(workflow: fmk.Workflow) -> fmk.Workflow:
    """
    Displays the workflow attributes and returns the workflow
    """
    
    print(workflow)
    print(f'Parallelism: \t\t{workflow.parallelism}')
    print(f'Dependency Complexity: \t{workflow.complexity}')
    return workflow

while engine.running:
    draw_workflow(current_workflow)

    if engine.keys[bsk.pg.K_1] and not engine.prev_keys[bsk.pg.K_1]: 
        current_workflow = select_workflow(workflow_1)
    if engine.keys[bsk.pg.K_2] and not engine.prev_keys[bsk.pg.K_2]: 
        current_workflow = select_workflow(workflow_2)
    if engine.keys[bsk.pg.K_3] and not engine.prev_keys[bsk.pg.K_3]: 
        current_workflow = select_workflow(workflow_3)        

    engine.update()
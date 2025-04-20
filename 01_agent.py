import framework as fmk

print('Agent actions:\n' \
'  Send : Sends a message\n' \
'  Set <key> <value>: Sets a context resource \n' \
'  Get <key> : Gets a context resource\n' \
'  Add-Task : Adds a new task' \
'  Deregister <id> : Removes an agent')

agent = fmk.Agent()

while True:
    message = input('Enter action: ').split(' ')

    match message[0].lower():
        case 'send':
            content  = input('Enter the message: ')
            recivers = [int(rec) for rec in filter(lambda x: x, input('Enter the recivers: ').split(' '))]
            msg = fmk.Message(content=content, recivers=recivers)
            agent.send(msg)
        case 'register':
            msg = fmk.Message(type='tool', content='register')
            agent.send(msg)
        case 'deregister':
            id = message[1]
            msg = fmk.Message(type='tool', content='deregister', resources=[id])
            agent.send(msg)
        case 'set':
            key   = message[1]
            value = message[2]
            msg = fmk.Message(type='tool', content='set resource', resources=[key, value])
            agent.send(msg)
        case 'get':
            key = message[1]
            msg = fmk.Message(type='tool', content='get resource', resources=[key])
            agent.send(msg)
        case 'remove':
            key = message[1]
            msg = fmk.Message(type='tool', content='remove resource', resources=[key])
            agent.send(msg)
        case 'add-task':
            specifications = input('Enter the task specifications: ')
            dependencies = [int(dep) for dep in filter(lambda x: x, input('Enter any dependencies: ').split(' '))]
            msg = fmk.Message(type='tool', content='add task', resources=[specifications, dependencies])
            agent.send(msg)
        case 'get-task':
            task_id = message[1]
            msg = fmk.Message(type='tool', content='get task', resources=[task_id])
            agent.send(msg)
        case _:
            print('Invalid action')
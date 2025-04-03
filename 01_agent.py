import framework as fmk

print('Agent actions:\n' \
'  Send : Sends a message\n' \
'  Set <key> <value>: Sets a context resource \n' \
'  Get <key> : Gets a context resource\n' \
'  Add-Task : Adds a new task')

agent = fmk.Agent()

while True:
    message = input('Enter action: ').split(' ')

    match message[0].lower():
        case 'send':
            content  = input('Enter the message: ')
            recivers = [int(rec) for rec in filter(lambda x: x, input('Enter the recivers: ').split(' '))]
            agent.send(content=content, recivers=recivers)
        case 'set':
            key   = message[1]
            value = message[2]
            agent.send(type='tool', content='set resource', data=[key, value])
        case 'get':
            key = message[1]
            agent.send(type='tool', content='get resource', data=[key])
        case 'add-task':
            specifications = input('Enter the task specifications: ')
            dependencies = [int(dep) for dep in filter(lambda x: x, input('Enter any dependencies: ').split(' '))]
            agent.send(type='tool', content='add task', data=[specifications, dependencies])
        case _:
            print('Invalid action')
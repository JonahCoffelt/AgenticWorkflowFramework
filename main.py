import framework as fmk

ctx = fmk.Context()

agent = fmk.Agent()
ctx.register(agent)

with open('sample_message.json', 'r') as file:
    mes = file.read()
    ctx.send(mes)
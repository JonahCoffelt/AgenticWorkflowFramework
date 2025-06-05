import framework as fmk

# Change to specifications
# role = input("What is the role of this agent: ")
task = int(input("Which task: "))
agent = fmk.LLMAgent("Do tasks. ", task)
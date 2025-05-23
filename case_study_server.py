import time
from threading import Thread
import framework as fmk
from case_study_classes import ControllableLoad, NonControllableLoad, Generator



class CaseStudy:
    def __init__(self):
        self.ctx = fmk.Context()

        self.set_loads(100, 50)
        self.set_generators()
        
        self.set_tasks()
        time.sleep(0.5)
        self.add_agents()
        time.sleep(0.5)

        self.ctx.set_task_status((None, None), self.initial_task, 1)
        self.ctx.send_message(fmk.Message("Start your task", recivers=[1]))

    def set_loads(self, non_controllable: float, controllable:float):
        """Using a controllable and non controllable load"""
        self.non_controllable_load = NonControllableLoad(non_controllable)
        self.controllable_load     = ControllableLoad   (controllable)

    def set_generators(self):
        """Set an arbitrary amount of generators"""

        wind   = Generator(5, 10)
        diesel = Generator(10, 20)
        pv     = Generator(2, 15)
        ess    = Generator(-1, 30)

        self.generators = [wind, diesel, pv, ess]

    def set_tasks(self) -> None:
        """Creates all the tasks in the case study"""
        
        self.initial_task = self.ctx.add_task(None, "Request a load from the smart grid. Some amount between 10-20W. Set the output of this task to the request amount.", [])

        self.generator_tasks = []
        for generator in self.generators:
            spec = f"Send some energy. Input is the total amount needed. Your cost is {generator.cost} per W. Your rate is {generator.rate} W per hour. The output of this task should be a numeric value. "
            task = self.ctx.add_task(None, spec, [self.initial_task])
            self.generator_tasks.append(task)
        
        self.confirmation_task = self.ctx.add_task(None, "Report the total amount recived from all the generators. Each input to your task is an energy amount. ", self.generator_tasks)

    def add_agents(self):
        prompt = f"You are a load requester in a microgrid. "
        agent = Thread(self.add_agent(prompt, self.initial_task), args=(prompt, self.initial_task))
        agent.start()
        
        for task in self.generator_tasks:
            prompt = f"You are a generator controller in a microgrid. Your task is to send out energy based on the system. There are {len(self.generators)} other generators. "
            agent = Thread(self.add_agent(prompt, task), args=(prompt, task))
            agent.start()

        prompt = f"You are reporting energy recived in a microgrid system. "
        agent = Thread(self.add_agent(prompt, self.confirmation_task), args=(prompt, self.confirmation_task))
        agent.start()

    def add_agent(self, prompt, task):
        fmk.LLMAgent(prompt, task)

app = CaseStudy()
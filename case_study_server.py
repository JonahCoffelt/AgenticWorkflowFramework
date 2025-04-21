import framework as fmk
from case_study_classes import ControllableLoad, NonControllableLoad, Generator
import time


class CaseStudy:
    def __init__(self):
        self.ctx = fmk.Context()
        time.sleep(.01)

        self.set_loads(100, 50)
        self.set_generators()
        self.set_tasks()

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

    def set_tasks(self):
        """Creates all the tasks in the case study"""
        
        initial_task = self.ctx.add_task(None, "Request a load from the smart grid.", [])

        generator_tasks = []
        for generator in self.generators:
            spec = f"Send some energy. Input is the total amount needed. Your cost is {generator.cost} per W. Your rate is {generator.rate} W per hour"
            generator_tasks.append(self.ctx.add_task(None, spec, [initial_task]))
        
        confirmation_task = self.ctx.add_task(None, "Confirm the current projections. Either re-request energy, adjust the load, or confirm.", [initial_task, *generator_tasks])


app = CaseStudy()
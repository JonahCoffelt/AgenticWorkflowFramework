class Load:
    def __init__(self, amount: float):
        self.load = amount

    def get(self): return self.load

class NonControllableLoad(Load):
    def __init__(self, amount):
        super().__init__(amount)

class ControllableLoad(Load):
    def __init__(self, amount):
        super().__init__(amount)

    def set(self, amount: float): self.load = amount


class Generator:
    def __init__(self, rate: float, cost: float):
        self.rate = rate
        self.cost = cost

    def get_cost(self, amount: float) -> float:
        """Get the cost of a given amount from this generator"""
        return self.cost * amount
    
    def get_time(self, amount: float) -> float:
        """Get the time required to generate a given amount using this generator"""
        return amount / self.rate
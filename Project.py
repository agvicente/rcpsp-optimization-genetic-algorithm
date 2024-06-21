import numpy as np

class Resource:
    def __init__(self, name: str, per_period_availability: int):
        self.name = name
        self.per_period_availability = per_period_availability

class Task:
    def __init__(self, name: str, predecessors: np.ndarray['Task'], sucessors: np.ndarray['Task'], duration: int, renewable_resources: np.ndarray[int]):
        self.name = name
        self.predecessors = predecessors
        self.sucessors = sucessors
        self.duration = duration
        self.renewable_resources = renewable_resources

class Schedule:
    def __init__(self, tasks: np.ndarray[Task], renewable_resources: np.ndarray[Resource]):
        self.dummySource = Task("Dummy Source", [], [], 0)
        self.dummySink = Task("Dummy Sink", [], [], 0)
        self.tasks = tasks
        self.renewable_resources = renewable_resources
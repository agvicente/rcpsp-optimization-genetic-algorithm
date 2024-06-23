import numpy as np

class Task:
    def __init__(
            self, 
            name: str,
            duration: int = 0, 
            renewable_resources: np.ndarray[int] = [],
            earliest_start: int = 0,
            earliest_finish: int = 0,
            latest_start: int = 0,
            latest_finish: int = 0
    ):
        self.name = name
        self.predecessors = []
        self.sucessors = []
        self.duration = duration
        self.renewable_resources = renewable_resources
        self.earliest_start = earliest_start
        self.earliest_finish = earliest_finish
        self.latest_start = latest_start
        self.latest_finish = latest_finish
    
    def add_predecessor(
            self, 
            task: 'Task'
    ):
        self.predecessors = np.append(self.predecessors, task)
        task.sucessors = np.append(task.sucessors, self)
    
    def add_sucessor(
            self, 
            task: 'Task'
    ):
        self.sucessors = np.append(self.sucessors, task)
        task.predecessors = np.append(task.predecessors, self)
    
    def add_predecessors(
            self, 
            tasks: np.ndarray['Task']
    ):
        for task in tasks:
            self.add_predecessor(task)

    
    def add_sucessors(
            self, 
            tasks: np.ndarray['Task']
    ):
        for task in tasks:
            self.__add_sucessor(task)
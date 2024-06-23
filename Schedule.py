import numpy as np
from Task import Task
from Resource import Resource

class Schedule:
    def __init__(
            self,
    ) -> None:
        self.dummySource = Task("Dummy Source", 0, [], 0, 0, 0, 0)
        self.dummySink = Task("Dummy Sink", 0, [], 0, 0, 0, 0)
        self.dummySink.add_predecessor(self.dummySource)
        self.tasks = []
        self.renewable_resources = []
        self.tasks.append(self.dummySource)
        self.tasks.append(self.dummySink)
    
    def add_task(
            self, 
            task: Task
    ):
        task.add_predecessor(self.dummySource)
        task.add_sucessor(self.dummySink)
        self.tasks = self.tasks[:-1]
        self.tasks = np.append(self.tasks, task)
        self.tasks = np.append(self.tasks, self.dummySink)

    def add_tasks(
            self, 
            tasks: np.ndarray[Task]
    ):
        for task in tasks:
            self.add_task(task)

    def add_renewable_resource(
            self, 
            resource: Resource
    ):
        self.renewable_resources = np.append(self.renewable_resources, resource)

    
    def is_valid_precedence_relations_constraint(self) -> bool:
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            subarray = self.tasks[:i]
            for predecessor in task.predecessors:
                if predecessor not in subarray:
                    return False
            
        return True
    
    def is_valid_duplicate_tasks_constraint(self) -> bool:
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            subarray = self.tasks[:i]
            if task in subarray:
                return False
        
        return True
    
    def forward_recursion(self) -> bool:
        if(not self.is_valid_precedence_relations_constraint):
            return False

        if(not self.is_valid_duplicate_tasks_constraint):
            return False

        for task in self.tasks:
            if(task == self.dummySource):
                task.earliest_start = 0
                task.earliest_finish = 0
            else:
                earliest_start = np.max([predecessor.earliest_finish for predecessor in task.predecessors])
                earliest_finish = earliest_start + task.duration
                task.earliest_start = earliest_start
                task.earliest_finish = earliest_finish
    
        return True


    def backward_recursion(self) -> bool:
        if(not self.is_valid_precedence_relations_constraint):
            return False

        if(not self.is_valid_duplicate_tasks_constraint):
            return False
        
        self.forward_recursion()
        self.dummySink.latest_finish = self.dummySink.earliest_finish
        self.dummySink.latest_start = self.dummySink.earliest_start
        for task in reversed(self.tasks):
            if(task == self.dummySink):
                continue
            latest_finish = np.min([sucessor.latest_start for sucessor in task.sucessors])
            latest_start = latest_finish - task.duration
            task.latest_finish = latest_finish
            task.latest_start = latest_start
        
        return True

    def makespan(self) -> int:
        self.forward_recursion()
        return self.dummySink.earliest_finish
    
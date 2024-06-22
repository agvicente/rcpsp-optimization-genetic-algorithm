import numpy as np

class Resource:
    def __init__(
            self, 
            name: str, 
            per_period_availability: int
    ) -> None:
        self.name = name
        self.per_period_availability = per_period_availability

class Task:
    def __init__(
            self, 
            name: str, 
            predecessors: np.ndarray['Task'] = [], 
            sucessors: np.ndarray['Task'] = [], 
            duration: int = 0, 
            renewable_resources: np.ndarray[int] = []
    ):
        self.name = name
        self.predecessors = predecessors
        self.sucessors = sucessors
        self.duration = duration
        self.renewable_resources = renewable_resources

class Schedule:
    def __init__(
            self, 
            renewable_resources: np.ndarray[Resource] = [], 
            tasks: np.ndarray[Task] = []
    ) -> None:
        self.dummySource = Task("Dummy Source", [], [], 0)
        self.dummySink = Task("Dummy Sink", [], [], 0)
        self.tasks = tasks
        self.renewable_resources = renewable_resources
        self.tasks.append(self.dummySource)
        self.tasks.append(self.dummySink)
    
    def add_task(
            self, 
            task: Task
    ):
        self.tasks = self.tasks[:-1]
        self.tasks = np.append(self.tasks, task)
        self.tasks = np.append(self.tasks, self.dummySink)

    def add_tasks(
            self, 
            tasks: np.ndarray[Task]
    ):
        self.tasks = self.tasks[:-1]
        self.tasks = np.append(self.tasks, tasks)
        self.tasks = np.append(self.tasks, self.dummySink)

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
    
    def forward_recursion(self):
        pass
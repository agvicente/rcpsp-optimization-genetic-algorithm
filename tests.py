from Project import Schedule, Task, Resource
import numpy as np

print('----------------------------------------------')
print('Test 1: Creating a Schedule object')

schedule = Schedule()

resource1 = Resource("Resource 1", 10)
resource2 = Resource("Resource 2", 20)

task1 = Task("Task 1", duration=5, renewable_resources=[resource1])
task2 = Task("Task 2", duration=10, renewable_resources=[resource2])

schedule.add_renewable_resource(resource1)
schedule.add_renewable_resource(resource2)

schedule.add_task(task1)
schedule.add_task(task2)

def print_tasks():
    for task in schedule.tasks:
        print(task.name)

print_tasks()


print('----------------------------------------------')

print('Test 2: Precedence relations')

task10 = Task("Task 10", duration=5, predecessors=[task1], renewable_resources=[resource1])
task11 = Task("Task 11", duration=5, predecessors=[task1], renewable_resources=[resource1])
task9 = Task("Task 9", duration=5, predecessors=[task1, task10, task11], renewable_resources=[resource1])
task4 = Task("Task 4", duration=10, predecessors=[task2], renewable_resources=[resource2])
task5 = Task("Task 5", duration=5, predecessors=[task2, task4], renewable_resources=[resource1, resource2])
task6 = Task("Task 6", duration=5, predecessors=[task5], renewable_resources=[resource1])
task8 = Task("Task 8", duration=5, predecessors=[task6], renewable_resources=[resource1])
task7 = Task("Task 7", duration=5, predecessors=[task8], renewable_resources=[resource2])
task3 = Task("Task 3", duration=5, predecessors=[task1], renewable_resources=[resource1])
task1 = Task("Task 1", duration=5, renewable_resources=[resource1])
task2 = Task("Task 2", duration=10, predecessors=[task1], renewable_resources=[resource2])

schedule.add_tasks([task3, task4, task5, task6, task8, task7, task9, task10, task11])

is_valid = schedule.is_valid_precedence_relations_constraint()

print_tasks()

print('Is valid:', is_valid)

print('----------------------------------------------')

print('Test 3: Duplicate tasks')

print('Is valid:', schedule.is_valid_duplicate_tasks_constraint())

print('----------------------------------------------')

print('All tests passed!')

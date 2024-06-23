from Schedule import Schedule
from Task import Task
from Resource import Resource
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

def print_tasks(schedule: Schedule):
    for task in schedule.tasks:
        print(task.name)

print_tasks(schedule)


print('----------------------------------------------')

print('Test 2: Precedence relations')

task10 = Task("Task 10", duration=5, renewable_resources=[resource1])
task11 = Task("Task 11", duration=5, renewable_resources=[resource1])
task9 = Task("Task 9", duration=5, renewable_resources=[resource1])
task4 = Task("Task 4", duration=10, renewable_resources=[resource2])
task5 = Task("Task 5", duration=5, renewable_resources=[resource1, resource2])
task6 = Task("Task 6", duration=5, renewable_resources=[resource1])
task8 = Task("Task 8", duration=5, renewable_resources=[resource1])
task7 = Task("Task 7", duration=5, renewable_resources=[resource2])
task3 = Task("Task 3", duration=5, renewable_resources=[resource1])
task1 = Task("Task 1", duration=5, renewable_resources=[resource1])
task2 = Task("Task 2", duration=10, renewable_resources=[resource2])

task10.add_predecessors([task1])
task11.add_predecessors([task1])
task9.add_predecessors([task1, task10, task11])
task4.add_predecessors([task2])
task5.add_predecessors([task2, task4])
task6.add_predecessors([task5])
task8.add_predecessors([task6])
task7.add_predecessors([task8])
task3.add_predecessors([task1])
task2.add_predecessors([task1])

schedule.add_tasks([task3, task4, task5, task6, task8, task7, task9, task10, task11])

is_valid = schedule.is_valid_precedence_relations_constraint()

print_tasks(schedule)

print('Is valid:', is_valid)

print('----------------------------------------------')

print('Test 3: Duplicate tasks')

print('Is valid:', schedule.is_valid_duplicate_tasks_constraint())

print('----------------------------------------------')


print('Test 4: Forward Recursion')

schedule2 = Schedule()

a1 = Task("A1", duration=4)
a2 = Task("A2", duration=3)
a3 = Task("A3", duration=2)
a4 = Task("A4", duration=5)

a2.add_predecessors([a1])
a3.add_predecessors([a1])
a4.add_predecessors([a2, a3])

schedule2.add_tasks([a1, a2, a3, a4])

schedule2.forward_recursion()

def print_time_windows_es_ef(schedule: Schedule):
    for task in schedule.tasks:
        print(task.name, [task.earliest_start, task.earliest_finish])

print_time_windows_es_ef(schedule2)

print('----------------------------------------------')

print('Test 5: Backward Recursion')

schedule3 = Schedule()

b1 = Task("B1", duration=4)
b2 = Task("B2", duration=3)
b3 = Task("B3", duration=2)
b4 = Task("B4", duration=5)

b2.add_predecessors([b1])
b3.add_predecessors([b1])
b4.add_predecessors([b2, b3])

schedule3.add_tasks([b1, b2, b3, b4])

# for task in schedule3.tasks:
#     print(task.name, [predecessor.name for predecessor in task.sucessors])

print(schedule3.backward_recursion())

def print_time_windows_ls_lf(schedule: Schedule):
    for task in schedule.tasks:
        print(task.name, [task.latest_start, task.latest_finish])

print_time_windows_ls_lf(schedule3)


print('----------------------------------------------')

print('Test 6: Makespan')

schedule4 = Schedule()

c1 = Task("C1", duration=4)
c2 = Task("C2", duration=3)
c3 = Task("C3", duration=2)
c4 = Task("C4", duration=5)

c2.add_predecessors([c1])
c3.add_predecessors([c1])
c4.add_predecessors([c2, c3])

schedule4.add_tasks([c1, c2, c3, c4])

print(schedule4.makespan())

print('----------------------------------------------')

print('All tests passed!')

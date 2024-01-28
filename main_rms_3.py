from src.task import TaskSet
from src.schedule import Schedule

if __name__ == '__main__':
    task_set = TaskSet(num_of_tasks=5, cpu_utilization=0.95, harmonic=False, filename="Tasks1")
    schedule = Schedule(task_dict=task_set.generated_task_dict, filename="Schedule1")

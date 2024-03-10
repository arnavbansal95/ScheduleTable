from src.task import TaskSet
from src.schedule import Schedule

if __name__ == '__main__':
    periods = [100, 200, 250, 350, 750]
    # task_set = TaskSet(num_of_tasks=5, cpu_utilization=0.95, harmonic=True, filename="Tasks1")
    task_set = TaskSet(num_of_tasks=5, input_periods=periods,
                       cpu_utilization=0.95, harmonic=True, filename="Tasks1")
    schedule = Schedule(task_dict=task_set.generated_task_dict, filename="Schedule1")

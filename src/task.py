import json
import math
import numpy as np
from drs import drs


class TaskSet:
    def __init__(self, num_of_tasks, cpu_utilization=0.9, harmonic=False, filename=None):
        self.num_of_tasks = num_of_tasks
        self.generated_periods_list = []
        self.generated_execution_time_list = []
        self.generated_task_dict = {}
        self.harmonic_tasks = harmonic
        self.cpu_utilization = cpu_utilization
        self.dict_filename = filename

        self.generate_periods()
        self.generate_execution_time()
        self.generate_dict()

        print("=" * 100)
        print("Generated TaskSet:")
        print("Periods of Tasks:\t\t\t" + str(self.generated_periods_list))
        print("Execution Time of Tasks:\t" + str(self.generated_execution_time_list))

    def generate_periods(self):
        raw_periods = np.random.uniform(5, 25, self.num_of_tasks)
        self.generated_periods_list = [int(x) for x in raw_periods]
        if self.harmonic_tasks:
            self.generated_periods_list = [math.floor(x / 5) * 5 for x in self.generated_periods_list]
        self.generated_periods_list.sort()  # For RMS Prio Assignment

    def generate_execution_time(self):
        task_utilization = drs(len(self.generated_periods_list), self.cpu_utilization)
        for idx in range(len(task_utilization)):
            self.generated_execution_time_list.append(round(task_utilization[idx] *
                                                            self.generated_periods_list[idx], 3))

    def generate_dict(self):
        for idx in range(len(self.generated_periods_list)):
            task_name = "OsTask_" + str(idx + 1)
            self.generated_task_dict[task_name] = dict(ExecTime=self.generated_execution_time_list[idx],
                                                       Period=self.generated_periods_list[idx],
                                                       Priority=int(idx + 1))
        if self.dict_filename is not None:
            with open(self.dict_filename + ".json", "w") as f:
                f.write(json.dumps(self.generated_task_dict, indent=4))

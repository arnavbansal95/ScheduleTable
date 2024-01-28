import json
import math


class Schedule:
    def __init__(self, task_dict, filename=None):
        self.input_task_dict = task_dict
        self.generated_schedule_dict = {}
        self.dict_filename = filename

        self.generate_scheduling_points()

        print("=" * 100)
        print("Generated Schedule:")
        print("Number of Scheduling Points:\t", len(self.generated_schedule_dict))

    def generate_scheduling_points(self):
        lcm_periods = math.lcm(*[x["Period"] for x in self.input_task_dict.values()])
        for idx in range(lcm_periods):
            temp_list = []
            for task in self.input_task_dict:
                if idx % self.input_task_dict[task]["Period"] == 0:
                    temp_list.append(task)
            if len(temp_list):
                self.generated_schedule_dict[idx] = temp_list

        if self.dict_filename is not None:
            with open(self.dict_filename + ".json", "w") as f:
                f.write(json.dumps(self.generated_schedule_dict, indent=4))

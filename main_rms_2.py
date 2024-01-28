import json
import math
from collections import OrderedDict

import numpy as np
from drs import drs

def generate_task_periods(num_of_tasks, harmonic=False):
    raw_periods = np.random.uniform(5, 25, num_of_tasks)
    generated_periods = [int(x) for x in raw_periods]
    if harmonic:
        generated_periods = [math.floor(x / 5) * 5 for x in generated_periods]
    generated_periods.sort()            # For RMS Prio Assignment
    return generated_periods

def generate_execution_time(input_period_list, cpu_utilization):
    generated_execution_time_list = []
    task_utilization = drs(len(input_period_list), cpu_utilization)
    for idx in range(len(task_utilization)):
        generated_execution_time_list.append(round(task_utilization[idx] * input_period_list[idx], 2))
    return generated_execution_time_list

def generate_task_dict(input_period_list, input_execution_time_list):
    generated_task_dict = {}
    for idx in range(len(input_period_list)):
        task_name = "OsTask_" + str(idx + 1) + "_" + str(input_period_list[idx]) + "ms"
        generated_task_dict[task_name] = dict(ExecTime=input_execution_time_list[idx],
                                              Period=input_period_list[idx],
                                              Priority=int(idx + 1))
    return generated_task_dict

def dict_to_json(input_dict, filename):
    with open(filename + ".json", "w") as f:
        f.write(json.dumps(input_dict, indent=4))

def generate_scheduling_points(input_task_dict):
    generated_schedule_dict = {}
    lcm_periods = math.lcm(*[x["Period"] for x in input_task_dict.values()])
    for idx in range(lcm_periods):
        temp_list = []
        for task in input_task_dict:
            if idx % input_task_dict[task]["Period"] == 0:
                temp_list.append(task)
        if len(temp_list):
            generated_schedule_dict[idx] = temp_list
    return generated_schedule_dict

def generate_schedule_table(input_schedule_dict, filename):
    temp_list = []
    final_str = ""
    multiplier = 1000000
    idx = 0
    for point in input_schedule_dict:
        offset_point = point * multiplier
        temp_list.append(list(input_schedule_dict.keys()).index(point))
        for task in input_schedule_dict[point]:
            if offset_point < 1000:
                temp_str = "\t\t" + str(offset_point) + ",\t\t\t\t" + "/* Offset */  \\\n"
            else:
                temp_str = "\t\t" + str(offset_point) + ",\t\t" + "/* Offset */  \\\n"
            temp_str += "\t\t" + "0,\t\t\t\t/* Max advance */  \\\n"
            temp_str += "\t\t" + "0,\t\t\t\t/* Max retard */  \\\n"
            temp_str += "\t\t" + "0,\t\t\t\t/* Event */  \\\n"
            temp_str += "\t\t" + str(task) + "\t" + "/* Task */  \\\n"
            temp_list.append(temp_str)
    for elem in temp_list:
        if type(elem) is int:
            final_str += "\t/* OsScheduleTableExpiryPoint_" + str(elem) + " */  \\\n"
        else:
            final_str += str("\t{  \\\n") + elem + str("\t},  \\\n")
    final_str = final_str.rstrip("\t},  \\\n") + "\n\t}"
    with open(filename + ".h", "w") as f:
        f.write(final_str)

if __name__ == '__main__':
    # period_list = generate_task_periods(num_of_tasks=3, harmonic=False)
    period_list = [3, 5, 7]
    execution_time_list = generate_execution_time(input_period_list=period_list, cpu_utilization=0.90)
    task_dict = generate_task_dict(input_period_list=period_list, input_execution_time_list=execution_time_list)
    dict_to_json(input_dict=task_dict, filename="Tasks")
    schedule_dict = generate_scheduling_points(input_task_dict=task_dict)
    dict_to_json(input_dict=schedule_dict, filename="Schedule")
    generate_schedule_table(input_schedule_dict=schedule_dict, filename="OsSchedule")

# Rate Monotonic Scheduling Example
import math
import pandas as pd
import plotly.figure_factory as ff
from collections import OrderedDict

# Task_Set = [t(C, T)] :-> C - ExecutionTime, T - TimePeriod
# raw_task_set = [(3, 20), (2, 5), (2, 10)]         # Example 1
# raw_task_set = [(1, 4), (2, 6), (3, 10)]          # Example 2
raw_task_set = [(19, 500), (5, 400), (36, 1000)]    # Example 3

def prio_assignment(input_task_set):
    tasks_dict = {}
    prio_weighed_tasks_list = []
    for idx in range(len(input_task_set)):
        task_key = "T" + str(idx + 1)
        tasks_dict[task_key] = input_task_set[idx]                          # Assign TaskName to Tasks
    print("=" * 100)
    print("Consider the Following Naming Convention for Given TaskSet")
    for task in tasks_dict:
        print(str(task) + ":\t" + str(tasks_dict[task]))
    print("=" * 100)
    for task in tasks_dict:
        prio_weighed_tasks_list.append((tasks_dict[task][1], task))
    prio_weighed_tasks_dict = dict(prio_weighed_tasks_list)                 # Sorting the TaskSet Based on Prio
    prio_weighed_tasks_dict = dict(OrderedDict(sorted(prio_weighed_tasks_dict.items())))
    temp_dict = {}
    for key in prio_weighed_tasks_dict.keys():
        temp_dict[prio_weighed_tasks_dict[key]] = tasks_dict[prio_weighed_tasks_dict[key]]
    tasks_dict = temp_dict
    print("Based on RMS Convention, Prio for Given TaskSet")
    temp_str = ""
    for task in tasks_dict:
        temp_str += str(task) + " > "
    temp_str = temp_str.strip(" > ")
    print(temp_str)
    print("=" * 100)
    return tasks_dict

def generate_scheduling_timeline(input_prio_weighed_task_set):
    task_periods = [int(x[1]) for x in input_prio_weighed_task_set.values()]    # Task Periods Extraction
    lcm_task_periods = math.lcm(*task_periods)                                  # Range for Scheduling Points
    timeline_list = ["Tx"] * lcm_task_periods                                   # Timeline List
    execution_list = [[x] * int(input_prio_weighed_task_set[x][0]) for x in input_prio_weighed_task_set]
    execution_list = sum(execution_list, [])
    for idx in range(len(timeline_list)):
        if idx == 0:
            timeline_list[idx] = execution_list[0]
            execution_list = execution_list[1:]
        if idx > 0:
            temp_list = []
            for task in input_prio_weighed_task_set:
                temp_int = int(idx) % input_prio_weighed_task_set[task][1]
                if temp_int == 0:
                    for power in range(input_prio_weighed_task_set[task][0]):
                        temp_list.append(task)
            if len(temp_list):
                execution_list = temp_list + execution_list
            if len(execution_list):
                timeline_list[idx] = execution_list[0]
                execution_list = execution_list[1:]
    return timeline_list

def generate_gantt_chart(input_timeline_list):
    dataframe_list = []
    print("Based on RMS Convention, Timeline for Given TaskSet")
    for idx in range(len(input_timeline_list)):
        task = str(input_timeline_list[idx])
        if task == "Tx":
            task = "IDLE"
        start = idx
        finish = idx + 1
        print(str(start) + "-" + str(finish) + ":\t" + task)
        temp_dict = dict(Task=task, Start=start, Finish=finish, Resource=task)
        dataframe_list.append(temp_dict)
        # print(temp_dict)
    print("=" * 100)

    df = pd.DataFrame(dataframe_list)
    fig = ff.create_gantt(df, index_col='Resource', bar_width=0.4, show_colorbar=True, title="Schedule Table",
                          group_tasks=True)
    fig.update_layout(xaxis_type='linear', autosize=False, width=1200, height=350)
    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor='black')
    for idx in range(len(input_timeline_list) + 1):
        fig.add_vline(x=idx, line_width=1, line_color="black", line_dash="dash")
    fig.write_html('first_figure.html', auto_open=True)


if __name__ == '__main__':
    task_set = prio_assignment(input_task_set=raw_task_set)
    # timeline = generate_scheduling_timeline(input_prio_weighed_task_set=task_set)
    # generate_gantt_chart(input_timeline_list=timeline)

import math
import pandas as pd
import plotly.figure_factory as ff
from collections import OrderedDict

# Task_Set = [t(C, T, P)] :-> C - ExecutionTime, T - TimePeriod, P - Priority (1 - 255)
task_set = [(1, 5, 1), (1, 10, 2), (1, 15, 3), (1, 20, 4)]


def find_scheduling_points(input_task_set):
    scheduling_points = {}
    task_periods = [int(x[1]) for x in input_task_set]                      # Task Periods Extraction
    gcd_task_periods = math.gcd(*task_periods)                              # Step for Scheduling Points
    lcm_task_periods = math.lcm(*task_periods)                              # Range for Scheduling Points
    for i in range(0, lcm_task_periods, gcd_task_periods):
        scheduling_points[str(i)] = []
    return scheduling_points


def find_schedule_table(input_task_set, input_scheduling_points, prio_sort=True):
    tasks_dict = {}
    prio_weighed_tasks_list = []
    for idx in range(len(input_task_set)):
        task_key = "T" + str(idx + 1)
        tasks_dict[task_key] = input_task_set[idx]                          # Assign TaskName to Tasks
    if prio_sort:
        for task in tasks_dict:
            prio_weighed_tasks_list.append((tasks_dict[task][2], task))
        prio_weighed_tasks_dict = dict(prio_weighed_tasks_list)             # Sorting the TaskSet Based on Prio
        prio_weighed_tasks_dict = dict(OrderedDict(sorted(prio_weighed_tasks_dict.items())))
        temp_dict = {}
        for key in prio_weighed_tasks_dict.keys():
            temp_dict[prio_weighed_tasks_dict[key]] = tasks_dict[prio_weighed_tasks_dict[key]]
        tasks_dict = temp_dict
    for point in input_scheduling_points:
        test_point = int(point)
        for task in tasks_dict.keys():
            if (test_point % int(tasks_dict[task][1])) == 0:                # SchPoint % TimePeriod == 0
                input_scheduling_points[str(test_point)].append(task)       # Task to be Scheduled on Point


def create_schedule_table_gantt_chart(input_task_set, input_schedule_table):
    tasks_dict = {}
    dataframe_list = []
    for idx in range(len(input_task_set)):
        task_key = "T" + str(idx + 1)
        tasks_dict[task_key] = input_task_set[idx]                          # Assign TaskName to Tasks
    for point in input_schedule_table:                                      # Add Tasks to Scheduling Points
        start = int(point)
        for task in input_schedule_table[point]:
            finish = start + tasks_dict[task][0]
            temp_dict = dict(Task=task, Start=start, Finish=finish, Resource=task)
            start = finish
            dataframe_list.append(temp_dict)
            # print(temp_dict)

    df = pd.DataFrame(dataframe_list)
    fig = ff.create_gantt(df, index_col='Resource', bar_width=0.4, show_colorbar=True, title="Schedule Table",
                          group_tasks=True)
    fig.update_layout(xaxis_type='linear', autosize=False, width=1800, height=450)
    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor='black')
    for point in input_schedule_table:
        fig.add_vline(x=int(point), line_width=2, line_color="black")
    fig.show()

    '''df = pd.DataFrame([
        dict(Task="Task 1", Start=2, Finish=3, Resource="T1"),
        dict(Task="Task 2", Start=1, Finish=2, Resource="T2"),
        dict(Task="Task 3", Start=0, Finish=1, Resource="T3"),
        dict(Task="Task 3", Start=3, Finish=4, Resource="T3")
    ])

    fig = ff.create_gantt(df, index_col='Resource', bar_width=0.4, show_colorbar=True, title="Schedule Table",
                          group_tasks=True)
    fig.update_layout(xaxis_type='linear', autosize=False, width=800, height=400)
    fig.show()'''


if __name__ == '__main__':
    schedule_table = find_scheduling_points(input_task_set=task_set)
    find_schedule_table(input_task_set=task_set, input_scheduling_points=schedule_table)
    print(schedule_table)

    create_schedule_table_gantt_chart(input_task_set=task_set, input_schedule_table=schedule_table)
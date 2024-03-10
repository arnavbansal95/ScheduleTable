import json
import math
from datetime import date


class Schedule:
    def __init__(self, task_dict, filename=None):
        self.input_task_dict = task_dict
        self.generated_schedule_dict = {}
        self.dict_filename = filename

        self.generate_scheduling_points()
        self.generate_schedule_table()

        print("=" * 100)
        print("Generated Schedule:")
        print("Number of Scheduling Points:\t", len(self.generated_schedule_dict))
        print("=" * 100)

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

    def generate_schedule_table(self):
        temp_list = []
        final_str = ""
        multiplier = 1000000
        for point in self.generated_schedule_dict:
            offset_point = point * multiplier
            temp_list.append(list(self.generated_schedule_dict.keys()).index(point))
            for task in self.generated_schedule_dict[point]:
                if offset_point < 1000:
                    temp_str = "\t\t" + str(offset_point) + ",\t\t\t\t" + "/* Offset */  \\\n"
                else:
                    temp_str = "\t\t" + str(offset_point) + ",\t\t" + "/* Offset */  \\\n"
                temp_str += "\t\t" + "0,\t\t\t\t/* Max advance */  \\\n"
                temp_str += "\t\t" + "0,\t\t\t\t/* Max retard */  \\\n"
                temp_str += "\t\t" + "0,\t\t\t\t/* Event */  \\\n"
                temp_str += "\t\t" + str(task) + "\t\t" + "/* Task */  \\\n"
                temp_list.append(temp_str)
        for elem in temp_list:
            if type(elem) is int:
                final_str += "\t/* OsScheduleTableExpiryPoint_" + str(elem) + " */  \\\n"
            else:
                final_str += str("\t{  \\\n") + elem + str("\t},  \\\n")
        final_str = final_str.rstrip("\\\n").rstrip().rstrip(",")
        with open("src\\header.txt", "r") as f:
            header_str_file = f.read()
            header_str_file = header_str_file.replace("DATE_HERE", date.today().strftime("%d %b %Y"))
        header_str = header_str_file + "\n\n#define OS_NSTENTRIES " + str(len(self.generated_schedule_dict)) \
                     + "\n#define OS_STENTRIES\n\n "
        footer_str = "\n\n#endif\n"
        final_str = header_str + final_str + footer_str
        with open("Os_config_patches.h", "w") as f:
            f.write(final_str)

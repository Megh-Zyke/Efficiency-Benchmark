import os
import json
import numpy as np

location = "testcases_generated"
files = os.listdir(location)
BIAS = 0.001  

for file_name in files:
    level_times = {0: [], 1: [], 2: [], 3: []}

    with open(f"{location}/{file_name}", "r") as file:
        data = json.load(file)

        for testcase in data.values():
            level = testcase["level"]
            exec_time = testcase["excecution_time"] + BIAS
            level_times[level].append(exec_time)

    execution_time_info = {}

    OPTIMAL_THRESHOLD_FACTOR = 1.5
    NORMAL_THRESHOLD_FACTOR = 2.0

    for level in range(4):
        if level_times[level]:
            optimal_time = np.percentile(level_times[level], 10)
            normal_time = np.median(level_times[level])
            
            optimal_threshold = optimal_time * OPTIMAL_THRESHOLD_FACTOR
            normal_threshold = normal_time * NORMAL_THRESHOLD_FACTOR
        else:
            optimal_time, normal_time, optimal_threshold, normal_threshold = None, None, None, None

        execution_time_info[f"level_{level}"] = {
            "optimal_time": optimal_time,
            "normal_time": normal_time,
            "optimal_threshold": optimal_threshold,
            "normal_threshold": normal_threshold
        }

    data["execution_time_info"] = execution_time_info

    with open(f"{location}/{file_name}", "w") as file:
        json.dump(data, file, indent=4)


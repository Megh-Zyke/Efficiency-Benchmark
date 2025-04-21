import json 
import os

json_file_path = "data/qwen-qwq-32b.json"

if os.path.exists(json_file_path):
    with open(json_file_path, "r") as f:
        data = json.load(f)

not_present = [6,8,9,10,11,13,14,15,16,18,19,20,23,26,27,29,30,31,34,36,37,39,40,41,42,43,44,45]

dicts = {}

for i in not_present:
    code = input(f"Please provide the code for Solution_{i}: ")
    dicts[f"Solution_" + {i}] = code

with open("data", "w")  as f:
    json.dump(dicts, f, indent=4)
    print(f"Data successfully written to {json_file_path}")
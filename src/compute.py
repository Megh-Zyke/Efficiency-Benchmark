import sys
import os
import ast
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
from typing import List
from datasets import load_dataset
import subprocess
import psutil

#sub section of the code 
code_ending = """
question_id = {question_id}
inputs = {test_case}

inputs = list(inputs.values())
if question_id == 35:
    inputs = [list_to_linked_list(inputs[0]), (inputs)[1]]
if question_id in [10]:
    res = []
    for i in inputs:
        for j in i:
            res.append(list_to_linked_list(j))
    inputs = [res]
if question_id == 15:
    res = []
    for j in inputs:
        res.append(build_graph(j))
    inputs = res
if question_id in [17 , 36 , 37, 38, 39]:
    res = []
    for j in inputs:
        res.append(list_to_tree(j))
    inputs = res
time_limit = {time_limit}
memory_limit = {memory_limit}
def solve():
    solution = Solution()
    tracemalloc.start()
    start_time = time.time()
    result = solution.{method_name}(*inputs)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    exec_time = end_time - start_time
    peak_memory = peak / 1024 

    if question_id in [10, 35]:  
        result = linked_list_to_list(result)
    if question_id == 15:   
        result = graph_to_adj_list(result)
    if question_id == 40:
        result = tree_to_list(result)
    
    return {{
        "result": result,
        "exec_time": exec_time if exec_time < time_limit else "Time Limit Exceeded",
        "peak_memory": peak_memory ,
        "status": "SUCCESS" if (exec_time < time_limit) else "FAILURE"
    }}

print(json.dumps(solve()))
"""
#function to get datasets and test cases
def dataset_load():
    ds = load_dataset("meghssss/effiBenchmarking")
    for _ in tqdm(range(1), desc="Loading dataset"):
        pass  # Simulate progress bar for loading
    return pd.DataFrame(ds["train"])

df = dataset_load()

# Function to get test cases and efficiency metrics for a given question name
def get_values(question_name):
    question_name = question_name.replace("_", " ")[:-5].capitalize()
    index_value = df[df["name"] == question_name].index[0]
    return ast.literal_eval(df["testcases"][index_value]) , ast.literal_eval(df["eff_metrics"][index_value])

#Function to compute the score of a program based on time and memory usage

def score(ai_time , optimal_time , threshold_time , ai_memory , threshold_memory , alpha = 1.875 , beta = 1 , w_t = 0.6 , w_m = 0.4):
    # Time Score with Progressive Penalty
    BIAS = 1e-6
    ai_time = max(ai_time, BIAS)
    ai_memory = max(ai_memory, BIAS)
    threshold_memory = max(threshold_memory, BIAS)
    threshold_time = max(threshold_time, BIAS)
    optimal_time = max(optimal_time, BIAS)

    time_ratio = max(1e-6, ai_time / optimal_time)
    
    if ai_time > threshold_time:
        time_penalty = 1 + alpha * ((ai_time - threshold_time) / threshold_time)
    else:
        time_penalty = 1

    time_score =  min(1, 1 / (time_ratio * time_penalty))

    # Memory Score with Separate Penalty
    if ai_memory > threshold_memory:
        memory_penalty = 1 + beta * ((ai_memory - threshold_memory) / threshold_memory)
    else:
        memory_penalty = 1

    memory_score =  min(1, threshold_memory / (ai_memory * memory_penalty))

    # Final Score: Weighted Geometric Mean
    final_score = (time_score**w_t * memory_score**w_m)**(1 / (w_t + w_m))

    return final_score

# Function to compute the efficiency score and pass rate for a given DataFrame
def computeScore(filename):
    efficiency_score = filename.groupby("question")["score"].mean().mean()
    scores = []
    pass_scores = filename.groupby("question")["pass"].apply(list).reset_index()
    for i in range(len(pass_scores)):
        count = 0
        pass_val = 0
        for val in pass_scores["pass"][i]:
            if val:
                pass_val += 1
            count += 1
        scores.append(pass_val/count)

    return np.mean(scores) , efficiency_score



# Function to forcefully kill a process and its children (Windows)
def kill_process_and_children(pid):
    try:
        process = psutil.Process(pid)
        for child in process.children(recursive=True):
            child.kill()
        process.kill()
    except psutil.NoSuchProcess:
        pass  # Ignore if the process already terminated

# Function to execute code in an isolated process
def execute_code_in_isolation(file_path ):
    process = None
    status = "SUCCESS"
    try:
        # Launch the Python code as a subprocess
        process = subprocess.Popen(
            ['python', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Monitor the process in real-time
        try:
            stdout, stderr = process.communicate(timeout = 5)  # Set a timeout for the process
        except subprocess.TimeoutExpired:
            kill_process_and_children(process.pid)
            return None, "TIME_LIMIT_EXCEEDED"
        
        if stderr and "Traceback" in stderr:
            return None, stderr.strip().split('\n')[-1]
            
        return stdout.strip(), status
    except Exception as e:
        if process:
            kill_process_and_children(process.pid)
        return None, str(e)

file_path = f"./tmp/test.py"
os.makedirs("./tmp", exist_ok=True)

# Read and save imports from a file
def read_imports(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        imports = file.read()
    return imports

# Example usage
imports_file_path = "./src/imports.txt"
imports_list = read_imports(imports_file_path)

# Load questions from Excel file
data_path = "./benchmark_prototype.xlsx"
data = pd.read_excel(data_path)
questions = data["question"]

#Compute the score of a given file 
def compute_score(filename):
    """Computes the score of the generated code."""
    # Load the generated code
    path = "data/" + filename
    try:
        with open(path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("File is not a valid JSON")
        
    solution_json = [] #list to hold the information and convert it to a csv table for further analysis

    for question, solution in data.items():

        question_id = int(question.split("_")[1])
        question_filename = questions[question_id].lower().replace(" ", "_") + ".json"
        print(f"Checking solution for {questions[question_id]}...")

        solution_code = imports_list + "\nclass Solution:\n" + solution.split("class Solution:\n")[1]
        
        try:
            testcases , timeLimit = get_values(question_filename)
        except IndexError:
            print(f"Test case file not found. Skipping...")
            continue 

        exec_globals = {}
        try:
            exec(solution_code, exec_globals)
        except Exception as e:
            print(f"Error executing solution for {question}: {e}")
            continue
        
        # Check if class Solution exists
        if "Solution" not in exec_globals:
            print(f"Solution class not found in {question}. Skipping...")
            continue
        solution_instance = exec_globals["Solution"]()

        for test_id, testcase in tqdm(testcases.items()):
                if not isinstance(testcase, dict) or "inputs" not in testcase:
                    continue  # Skip non-testcase entries
                level = testcase["level"]        
                inputs = testcase["inputs"]
                expected_output = testcase["output"]
                
                method_name = list(solution_instance.__class__.__dict__.keys())[1]  #first method is the target

                time_limit = timeLimit[f"level_{level}"]["normal_threshold"] 
                optimal_time = timeLimit[f"level_{level}"]["optimal_time"]
                memory_limit = timeLimit[f"level_{level}"]["normal_memory_threshold"]
                final_code = solution_code + code_ending.format(
                    question_id=question_id,
                    test_case= inputs,
                    method_name=method_name,
                    time_limit=time_limit,
                    memory_limit=memory_limit,
                )
                with open(file_path, "w") as f:
                     f.write(final_code)

                     # Execute the code
                output, status = execute_code_in_isolation(file_path)
                try:
                    output = json.loads(output)
                except:
                    continue
                if status == "SUCCESS":

                    try:
                        exec_time = float(output["exec_time"])
                        peak_memory = float(output["peak_memory"])
                        is_pass = expected_output == output["result"] and output["status"] == "SUCCESS"
                        sc = score(exec_time, optimal_time, time_limit, peak_memory, memory_limit if is_pass else 0)
                    except:
                        exec_time = 0
                        peak_memory = 0
                        is_pass = False
                        sc = 0

                    solution_json.append({
                            "question": question,
                            "test_id": test_id,
                            "pass": is_pass,
                            "exec_time": exec_time,
                            "peak_memory": peak_memory,
                            "exception_error": "" if is_pass else "Time or Memory Limit Exceeded",
                            "score": sc
                        })

                else:
                    solution_json.append({"question": question,
                                         "test_id": test_id, 
                                         "pass": False,
                                         "exec_time": 0, 
                                         "peak_memory": 0, 
                                         "exception_error": status,
                                         "score" : 0})
                        
                        
# Clean up the temporary file
    os.remove(file_path)
    df = pd.DataFrame(solution_json)
    output_csv_path = f"./results/{filename.replace('.json', '.csv')}"
    os.makedirs('./results', exist_ok=True)
    df.to_csv(output_csv_path, index=False) 

    pass_1 , efficiency_score = computeScore(df)
    print(f"pass@1: {pass_1}\nEfficiency Score: {efficiency_score}\nTotal Score : {pass_1*efficiency_score}")

compute_score("llama-3.3-70b.json")
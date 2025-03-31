import sys
import os
import ast
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import pandas as pd
import numpy as np
import json
import threading
import tracemalloc
import inspect
from tqdm import tqdm
from typing import List
from packages.ListToLinkedList import list_to_linked_list, linked_list_to_list
from packages.ListNode import ListNode
from packages.TreeNode import TreeNode, list_to_tree, tree_to_list
from packages.Node import Node, build_graph, graph_to_adj_list
from datasets import load_dataset
import subprocess
import psutil

#function to get datasets and test cases
def dataset_load():
    ds = load_dataset("meghssss/effiBenchmarking")
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
    ai_time += BIAS
    ai_memory += BIAS
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
def execute_code_in_isolation(file_path, timelimit , memory_limit ):
    process = None
    peak_memory = 0
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
        start_time = time.time()
        while process.poll() is None:
            current_time = time.time()

            # Track memory usage in real-time
            try:
                mem_info = psutil.Process(process.pid).memory_info().rss
                peak_memory = max(peak_memory, mem_info)
            except psutil.NoSuchProcess:
                break  # If the process terminated early

            # Handle timeouts
            if current_time - start_time > timelimit :
                kill_process_and_children(process.pid)
                status = "TIME_LIMIT_EXCEEDED"
                return None, status, peak_memory / 1024 / 1024 ,0

            # Handle memory limits
            # if peak_memory > memory_limit * 1024 * 1024:
            #     kill_process_and_children(process.pid)
            #     status = "MEMORY_LIMIT_EXCEEDED"
            #     return None, status, peak_memory / 1024 / 1024 ,time.time() - start_time

        # Capture output and error
        stdout, stderr = process.communicate()
        execution_time = time.time() - start_time

        if stderr:
            return None, stderr.strip(), peak_memory / 1024 / 1024 , 0

        return stdout.strip(), status, peak_memory / 1024 / 1024, execution_time

    except Exception as e:
        if process:
            kill_process_and_children(process.pid)
        return None, str(e), peak_memory / 1024 / 1024, 0


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

    total_tests = 0
    passed_tests = 0

    solution_json = [] #list to hold the information and convert it to a csv table for further analysis

    for question, solution in data.items():

        question_id = int(question.split("_")[1])
        question_filename = questions[question_id].lower().replace(" ", "_") + ".json"
        print(f"Checking solution for {questions[question_id]}...")

        solution_code = imports_list + "\nclass Solution:\n" + solution.split("class Solution:\n")[1]
        
        try:
            testcases , timelimit = get_values(question_filename)
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

        time_limits = {}
        memory_limits = {}
        optimal_time = {}
        for levels , val in timelimit.items():
            time_limits[levels] = val["normal_threshold"]
            memory_limits[levels] = val["normal_memory_threshold"]
            optimal_time[levels] = val["optimal_time"]

        for test_id, testcase in tqdm(testcases.items()):
                if not isinstance(testcase, dict) or "inputs" not in testcase:
                    continue  # Skip non-testcase entries

                level = testcase["level"]        
                inputs = testcase["inputs"].values()
                expected_output = testcase["output"]
                
                method_name = list(solution_instance.__class__.__dict__.keys())[1]  #first method is the target

                # Convert inputs to the appropriate types
                if question_id == 35:
                    inputs = [list_to_linked_list(list(inputs)[0]), list(inputs)[1]]

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
                # Extract method name from solution
                if question_id in [17 , 36 , 37, 38, 39]:
                    res = []
                    for j in inputs:
                        res.append(list_to_tree(j))
                    inputs = res
                
                solution_templates = {
                    10: """def solve():
    solution = Solution()
    result = solution.{method_name}({test_case})
    return linked_list_to_list(result)
print(solve())""",
                    15: """def solve():
    solution = Solution()
    result = solution.{method_name}({test_case})
    return graph_to_adj_list(result)
print(solve())""",
                    40: """def solve():
    solution = Solution()
    result = solution.{method_name}({test_case})
    return tree_to_list(result)
print(solve())"""
                }

                solution_string = solution_templates.get(
                    question_id,
                    """def solve():
    solution = Solution()
    result = solution.{method_name}({test_case})
    return result
print(solve())""")
                
                final_code = solution_code +"\n" + solution_string.format(
                    method_name=method_name,
                    test_case= inputs,
                )
                # Write the code file
                for test_case , value in testcases.items():
                    level = value["level"]
                    time_limt = timelimit[f"level_{level}"]["normal_threshold"]
                    memory_limit = timelimit[f"level_{level}"]["normal_memory_threshold"]


                    with open(file_path, "w") as f:
                        f.write(final_code)

                    # Execute the code
                    output, status, memory_usage, execution_time = execute_code_in_isolation(file_path, timelimit=time_limt, memory_limit=memory_limit)

                    # Print results
                    print("\nExecution Results:")
                    if status == "SUCCESS":
                        print(output)
                        # Check if output matches expected output
                        print(expected_output == ast.literal_eval(output))
                        print(f"Execution Time: {execution_time:.4f} sec")
                        print(f"Memory Usage: {memory_usage:.2f} MB")
                    else:
                        print(f"Error: {status}")

# Clean up the temporary file
    os.remove(file_path)

compute_score("groq_llama.json")
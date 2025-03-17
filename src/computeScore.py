import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import pandas as pd
import random
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


def run_with_timeout(method, inputs, level, time_limits, memory_limit_kb):  # Default 10MB limit
    result = None
    exception_error = ""
    peak_memory_kb = 0  # Store peak memory usage
    finished = threading.Event()
    
    def target():
        nonlocal result, exception_error, peak_memory_kb
        try:
            tracemalloc.start()
            result = method(*inputs)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            peak_memory_kb = peak / 1024  # Convert to KB
            if peak_memory_kb > memory_limit_kb:
                exception_error = "Memory limit exceeded"
        except Exception as e:
            result = None
            exception_error = f"{type(e).__name__}: {e}"
        finally:
            finished.set()

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(time_limits[level])

    if not finished.is_set():
        exception_error = "Time limit exceeded"
        result = None

    return result, exception_error, peak_memory_kb
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
        # Load corresponding test cases
        testcases_path = "./testcases_generated/" + question_filename

        try:
            with open(testcases_path, "r") as file:
                testcases = json.load(file)
        except FileNotFoundError:
            print(f"Test case file {testcases_path} not found. Skipping...")
            continue

        # Execute the generated solution dynamically
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
        testcase_solution = {}
        solution_instance = exec_globals["Solution"]()
        time_limits = {}
        memory_limits = {}
        for levels , val in testcases["execution_time_info"].items():
            time_limits[levels] = val["normal_threshold"]
            memory_limits[levels] = val["normal_memory_threshold"]

        for test_id, testcase in tqdm(testcases.items()):
                if not isinstance(testcase, dict) or "inputs" not in testcase:
                    continue  # Skip non-testcase entries

                level = testcase["level"]        
                inputs = testcase["inputs"].values()
                expected_output = testcase["output"]
               
                if question_id == 10:
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
                if question_id == 17:
                    res = []
                    for j in inputs:
                        res.append(list_to_tree(j))
                    inputs = res
                
                method_name = list(solution_instance.__class__.__dict__.keys())[1]  # Assuming first method is the target
                
                if hasattr(solution_instance, method_name):
                    method = getattr(solution_instance, method_name)
                    signature = inspect.signature(method)
                    exception_error = ""
                    
                    # Call method with the extracted inputs
                    
                
                    start_time = time.time()
                    result, exception_error, peak_memory = run_with_timeout(method, inputs, "level_" + str(level), time_limits , memory_limits["level_" + str(level)])
                    end_time = time.time()
                    exec_time = end_time - start_time
                    total_tests += 1

                    if question_id == 10:  
                        result = linked_list_to_list(result)

                    if question_id == 15:   
                        result = graph_to_adj_list(result)
                    
                    solution_json.append({"question": question,
                                         "test_id": test_id, 
                                         "pass": result == expected_output, 
                                         "exec_time": exec_time, 
                                         "peak_memory": peak_memory / 1024, 
                                         "exception_error": exception_error or ("Custom error: Output mismatch" if result != expected_output else "")})
                    if result == expected_output:
                        passed_tests += 1
    df = pd.DataFrame(solution_json)
    output_csv_path = f"./results/{filename.replace('.json', '.csv')}"
    os.makedirs('./results', exist_ok=True)
    df.to_csv(output_csv_path, index=False) 

# Run the function
compute_score("demo.json")
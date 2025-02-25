import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import pandas as pd
import random
import json
import tracemalloc
from typing import List, Optional
from collections import deque
import math
import heapq
from collections import defaultdict
from collections import Counter
from itertools import product
from heapq import heappop, heappush
from packages.ListToLinkedList import list_to_linked_list, linked_list_to_list
from packages.ListNode import ListNode
from packages.TreeNode import TreeNode, list_to_tree, tree_to_list
from packages.Node import Node, build_graph, graph_to_adj_list
import inspect


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

        solution_instance = exec_globals["Solution"]()
        for testcase in testcases.values():
            if "inputs" in testcase.keys():

                inputs = testcase["inputs"].values()
                expected_output = testcase["output"]
               
                if question_id == 10:
                    res = []
                    
                    for i in inputs:
                        for j in i:
                            res.append(list_to_linked_list(j))
                    inputs = [res]
                # Extract method name from solution
                method_name = list(solution_instance.__class__.__dict__.keys())[1]  # Assuming first method is the target
                
                if hasattr(solution_instance, method_name):
                    method = getattr(solution_instance, method_name)
                    signature = inspect.signature(method)
                    
                    # Call method with the extracted inputs
                    try:

                        result = method(*inputs)  # Unpacking input list
                    except Exception as e:
                        print(f"Runtime error for {question}: {e}")
                        continue

                    total_tests += 1

                    if question_id == 10:
                        
                        result = linked_list_to_list(result)
                        

                    if result == expected_output:
                        passed_tests += 1
                    else:
                        print(f"Test failed for {question}: Input: {inputs}, Expected: {expected_output}, Got: {result}")
        
        
        print(f"Total Tests: {total_tests}, Passed: {passed_tests}, Accuracy: {passed_tests / total_tests * 100:.2f}%")

# Run the function
compute_score("demo.json")

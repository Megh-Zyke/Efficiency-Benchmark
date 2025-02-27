import time
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


# Your given solution
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # Get the number of rows and columns in the matrix
        num_rows, num_columns = len(matrix), len(matrix[0])
      
        # Initialize pointers for the binary search
        left, right = 0, num_rows * num_columns - 1
      
        # Conduct a binary search in the matrix
        while left < right:
            # Calculate the middle index between left and right
            mid = (left + right) >> 1  # Equivalent to floor division by 2 (mid = (left + right) // 2)
            # Convert the 1D representation mid back to 2D indices x and y
            row, column = divmod(mid, num_columns)
            # If the middle element is greater or equal to the target, go left
            if matrix[row][column] >= target:
                right = mid
            # If the middle element is less than the target, go right
            else:
                left = mid + 1
      
        # After the loop, left should point to the target element if it exists
        # Check if the target is indeed at the (left // num_columns, left % num_columns) position
        return matrix[left // num_columns][left % num_columns] == target

# Define test cases
test_cases ==

# Function to run tests and measure performance
def run_tests():
    solution = Solution()
    results = {}

    for test_name, test in test_cases.items():
       
        inputs = test["inputs"]
     

        exc_time =  []
        memory = []
        # Start memory and time tracking
        
        for i in range(10):
            tracemalloc.start()
            start_time = time.time()

            # Run the function
            actual_output = solution.findMin(**inputs)

            # Stop memory and time tracking
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            exc_time.append(end_time - start_time)
            memory.append(peak)
        avg_time = sum(exc_time)/10
        peak = sum(memory)/10
        exc_time = []
        memory = []
        # Store results in the new dictionary format
        results[test_name] = {
            "level" : test["level"],
            "inputs": {
                "nums": inputs["nums"]
            },
            "output": actual_output,
            "excecution_time" : avg_time * 1000 ,
            "memory_used" : peak / 1024
        }

        # Print results to console
        print(f"Test: {test_name}")
        print(f"  Expected Output: {test['output']}")
        print(f"  Actual Output: {actual_output}")
        print(f"  Passed: {actual_output == test['output']}")
        print(f"  Execution Time: {avg_time * 1000} ms")
        print(f"  Memory Used: {round(peak / 1024, 4)} KB")
        print("-" * 50)

    return results

# Run the tests and collect results
test_results = run_tests()

# Save results to a JSON file
with open("testcases_generated/search_a_2d_matrixjson", "w") as file:
    json.dump(test_results, file, indent=4)

print("\n✅ Test results saved to 'test_results.json'!")
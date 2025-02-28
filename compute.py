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
    def maxArea(self, height: List[int]) -> int:
        l = 0
        r = len(height)-1
        maxarea = 0
        while l<r:
            maxarea = max(maxarea,(r-l)*(min(height[l],height[r])))
            if height[l]<height[r]:
                l+=1
            else:
                r-=1
# Define test cases
test_cases = {
    "test_case_1": {
        "level": 0,
        "inputs": {
            "height": [1, 8, 6, 2, 5, 4, 8, 3, 7]
        },
        "output": 49
    },
    "test_case_2": {
        "level": 0,
        "inputs": {
            "height": [1, 1]
        },
        "output": 1
    },
    "test_case_3": {
        "level": 0,
        "inputs": {
            "height": [4, 3, 2, 1, 4]
        },
        "output": 16
    },
    "test_case_4": {
        "level": 0,
        "inputs": {
            "height": [1, 2, 1]
        },
        "output": 2
    },
    "test_case_5": {
        "level": 0,
        "inputs": {
            "height": [2, 3, 10, 5, 7, 8, 9]
        },
        "output": 36
    },
    "test_case_6": {
        "level": 1,
        "inputs": {
            "height": [1, 1000, 1000, 1000, 1]
        },
        "output": 4000
    },
    "test_case_7": {
        "level": 1,
        "inputs": {
            "height": [2, 3, 10, 5, 7, 8, 9, 12, 1]
        },
        "output": 49
    },
    "test_case_8": {
        "level": 1,
        "inputs": {
            "height": [1, 2, 4, 3]
        },
        "output": 4
    },
    "test_case_9": {
        "level": 1,
        "inputs": {
            "height": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        },
        "output": 25
    },
    "test_case_10": {
        "level": 1,
        "inputs": {
            "height": [1000, 1, 1000, 1, 1000, 1, 1000]
        },
        "output": 6000
    },
    "test_case_11": {
        "level": 2,
        "inputs": {
            "height": [1000, 1, 1, 1, 1000]
        },
        "output": 4000
    },
    "test_case_12": {
        "level": 2,
        "inputs": {
            "height": [0, 0, 0, 0, 0, 0, 1000]
        },
        "output": 0
    },
    "test_case_13": {
        "level": 2,
        "inputs": {
            "height": [10000, 1, 1, 1, 1, 1, 10000]
        },
        "output": 60000
    },
    "test_case_14": {
        "level": 2,
        "inputs": {
            "height": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        },
        "output": 25
    },
    "test_case_15": {
        "level": 2,
        "inputs": {
            "height": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11]
        },
        "output": 100
    },
    "test_case_16": {
        "level": 3,
        "inputs": {
            "height": [i % 1000 for i in range(100000)]
        },
        "output": 99900000
    },
    "test_case_17": {
        "level": 3,
        "inputs": {
            "height": [10000] + [1] * 99998 + [10000]
        },
        "output": 999980000
    },
    "test_case_18": {
        "level": 3,
        "inputs": {
            "height": [i for i in range(100000)]
        },
        "output": 2499975000
    },
    "test_case_19": {
        "level": 3,
        "inputs": {
            "height": [i for i in range(100000, 0, -1)]
        },
        "output": 2499975000
    },
    "test_case_20": {
        "level": 3,
        "inputs": {
            "height": [10000 if i % 2 == 0 else 1 for i in range(100000)]
        },
        "output": 499950000
    }
}



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
            actual_output = solution.maxArea(**inputs)

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
                "height": inputs["height"]
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
with open("testcases_generated/container_with_most_water.json", "w") as file:
    json.dump(test_results, file, indent=4)

print("\n✅ Test results saved to 'test_results.json'!")
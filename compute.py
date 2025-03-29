import time
import random
import json
import tracemalloc
from typing import List, Optional,Tuple
from collections import deque
import math
from math import pi, isqrt
import heapq
import numpy as np
from collections import defaultdict
from collections import Counter
from itertools import product
from heapq import heappop, heappush
from packages.ListToLinkedList import list_to_linked_list, linked_list_to_list
from packages.ListNode import ListNode
from packages.TreeNode import TreeNode, list_to_tree, tree_to_list
from packages.Node import Node, build_graph, graph_to_adj_list
import re 
from cmath import exp

from typing import List
class Solution:
    def min_requests(self,n:int,requests: List[int]) -> int:
        # Initialize arrays for left and right passes
        lp = [0] * n          # Left pass (increasing part)
        rp = [0] * n          # Right pass (decreasing part)
        lnr = requests[:]     # Left normalized requests
        rnr = requests[:]     # Right normalized requests

        # Left pass: Ensure strictly increasing
        max_left = requests[0]
        for i in range(1, n):
            if requests[i] > max_left:
                max_left = requests[i]     # No extra requests needed
                lp[i] = lp[i - 1]
            else:
                max_left += 1
                lp[i] = lp[i - 1] + (max_left - requests[i])
            lnr[i] = max_left

        # Right pass: Ensure strictly decreasing
        max_right = requests[-1]
        for i in range(n - 2, -1, -1):
            if requests[i] > max_right:
                max_right = requests[i]    # No extra requests needed
                rp[i] = rp[i + 1]
            else:
                max_right += 1
                rp[i] = rp[i + 1] + (max_right - requests[i])
            rnr[i] = max_right

        # Calculate the minimum additional requests
        ans = min(rp[0], lp[-1])

        for i in range(1, n - 1):
            # Combine the left and right parts with a peak
            combined = lp[i - 1] + rp[i + 1]

            # Check if the peak needs additional requests
            max_peak = max(lnr[i - 1], rnr[i + 1]) + 1
            if max_peak > requests[i]:
                combined += max_peak - requests[i]

            ans = min(ans, combined)

        return ans

# Define test cases
test_cases = {
     "test_case_1": {
        "level": 0,
        "inputs": {
            "n": 1,
            "requests": [10]
        },
        "output": 0  # Already valid (single request)
    },
    "test_case_2": {
        "level": 0,
        "inputs": {
            "n": 2,
            "requests": [1, 2]
        },
        "output": 0  # Already valid (strictly increasing)
    },
    "test_case_3": {
        "level": 0,
        "inputs": {
            "n": 2,
            "requests": [2, 1]
        },
        "output": 0  # Already valid (strictly decreasing)
    },
    "test_case_4": {
        "level": 0,
        "inputs": {
            "n": 3,
            "requests": [1, 3, 2]
        },
        "output": 0  # Already valid (increasing then decreasing)
    },
    "test_case_5": {
        "level": 0,
        "inputs": {
            "n": 3,
            "requests": [2, 2, 1]
        },
        "output": 1  # Add 1 request at index 2 to make it strictly increasing
    },
    
    "test_case_6": {
        "level": 1,
        "inputs": {
            "n": 4,
            "requests": [1, 2, 2, 1]
        },
        "output": 1  # Add 1 request at index 2 to break the equal pair
    },
    "test_case_7": {
        "level": 1,
        "inputs": {
            "n": 5,
            "requests": [1, 4, 3, 2, 5]
        },
        "output": 6  # Add 2 requests at index 3, 4 requests at index 4
    },
    "test_case_8": {
        "level": 1,
        "inputs": {
            "n": 5,
            "requests": [5, 4, 3, 2, 1]
        },
        "output": 0  # Already valid (strictly decreasing)
    },
    "test_case_9": {
        "level": 1,
        "inputs": {
            "n": 6,
            "requests": [1, 2, 3, 3, 2, 1]
        },
        "output": 1  # Add 1 request at index 3
    },
    "test_case_10": {
        "level": 1,
        "inputs": {
            "n": 6,
            "requests": [1, 1, 1, 2, 3, 4]
        },
        "output": 2  # Add 2 requests at index 2 and 3
    },
    
   "test_case_11": {
        "level": 2,
        "inputs": {
            "n": 50,
            "requests": [i for i in range(1, 26)] + [i for i in range(24, 0, -1)]
        },
        "output": 0  # Already valid (perfect increase then decrease)
    },
    "test_case_12": {
        "level": 2,
        "inputs": {
            "n": 50,
            "requests": [2] * 50
        },
        "output": 49  # Add 1 request at each index to make it strictly increasing
    },
    "test_case_13": {
        "level": 2,
        "inputs": {
            "n": 100,
            "requests": [1 if i % 2 == 0 else 2 for i in range(100)]
        },
        "output": 50  # Add requests at every alternate index to break repeating pattern
    },
    "test_case_14": {
        "level": 2,
        "inputs": {
            "n": 100,
            "requests": [i % 10 + 1 for i in range(100)]
        },
        "output": 0  # Already valid (alternating increase-decrease)
    },
    "test_case_15": {
        "level": 2,
        "inputs": {
            "n": 100,
            "requests": [i // 2 + 1 for i in range(100)]
        },
        "output": 0  # Already valid (strictly increasing pattern)
    },
     "test_case_16": {
        "level": 3,
        "inputs": {
            "n": 10**5,
            "requests": [i for i in range(1, 50001)] + [i for i in range(50000, 0, -1)]
        },
        "output": 0  # Already valid (perfectly increasing and then decreasing)
    },
    "test_case_17": {
        "level": 3,
        "inputs": {
            "n": 10**5,
            "requests": [1] * 10**5
        },
        "output": 99999  # Add requests at each index to make it strictly increasing
    },
    "test_case_18": {
        "level": 3,
        "inputs": {
            "n": 10**5,
            "requests": [i % 5 + 1 for i in range(10**5)]
        },
        "output": 80000  # Many alternating requests need fixing
    },
    "test_case_19": {
        "level": 3,
        "inputs": {
            "n": 10**5,
            "requests": [2 if i % 2 == 0 else 1 for i in range(10**5)]
        },
        "output": 50000  # Half the requests need fixing
    },
    "test_case_20": {
        "level": 3,
        "inputs": {
            "n": 10**5,
            "requests": [i for i in range(1, 10**5 + 1)]
        },
        "output": 0  # Already valid (strictly increasing)
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
            actual_output = solution.min_requests(inputs["n"], inputs["requests"])
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
                "n": inputs["n"],
                "requests": inputs["requests"]
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
with open("testcases_generated/load_testing.json", "w") as file:
    json.dump(test_results, file, indent=4)

print("\n✅ Test results saved in testcases_generated!")
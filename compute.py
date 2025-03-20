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

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        nodes = []
        for lis in lists:
            while lis:
                nodes.append(lis.val)
                lis = lis.next
        
        head = ListNode(0)
        node = head
        for node_val in sorted(nodes):
            newnode = ListNode(node_val)
            node.next = newnode
            node = node.next
        
        return head.next
      
# Define test cases
test_cases = {
    "test_case_1": {
        "level": 0,
        "inputs": {
            "lists": [[1, 4, 5], [1, 3, 4], [2, 6]]
        },
        "output": [1, 1, 2, 3, 4, 4, 5, 6]
    },
    "test_case_2": {
        "level": 0,
        "inputs": {
            "lists": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        },
        "output": [1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    "test_case_3": {
        "level": 0,
        "inputs": {
            "lists": [[5, 10], [1, 2, 6], [3, 8]]
        },
        "output": [1, 2, 3, 5, 6, 8, 10]
    },
    "test_case_4": {
        "level": 0,
        "inputs": {
            "lists": [[1, 2], [3], [4, 5, 6]]
        },
        "output": [1, 2, 3, 4, 5, 6]
    },
    "test_case_5": {
        "level": 0,
        "inputs": {
            "lists": [[]]
        },
        "output": []
    },
    "test_case_6": {
        "level": 1,
        "inputs": {
            "lists": [[1, 3, 5], [2, 4, 6], [0, 7, 8]]
        },
        "output": [0, 1, 2, 3, 4, 5, 6, 7, 8]
    },
    "test_case_7": {
        "level": 1,
        "inputs": {
            "lists": [[10, 20, 30], [5, 15, 25], [2, 4, 6]]
        },
        "output": [2, 4, 5, 6, 10, 15, 20, 25, 30]
    },
    "test_case_8": {
        "level": 1,
        "inputs": {
            "lists": [[100, 200], [50, 150, 250], [1, 300]]
        },
        "output": [1, 50, 100, 150, 200, 250, 300]
    },
    "test_case_9": {
        "level": 1,
        "inputs": {
            "lists": [[1, 3], [2, 4], [], [5, 6]]
        },
        "output": [1, 2, 3, 4, 5, 6]
    },
    "test_case_10": {
        "level": 1,
        "inputs": {
            "lists": [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
        },
        "output": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    },
    "test_case_11": {
        "level": 2,
        "inputs": {
            "lists": [[1, 10, 100], [5, 50, 500], [2, 20, 200]]
        },
        "output": [1, 2, 5, 10, 20, 50, 100, 200, 500]
    },
    "test_case_12": {
        "level": 2,
        "inputs": {
            "lists": [[10, 20, 30, 40], [5, 15, 25, 35], [2, 12, 22, 32]]
        },
        "output": [2, 5, 10, 12, 15, 20, 22, 25, 30, 32, 35, 40]
    },
    "test_case_13": {
        "level": 2,
        "inputs": {
            "lists": [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        },
        "output": [1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    "test_case_14": {
        "level": 2,
        "inputs": {
            "lists": [[-10, -5, 0, 5, 10], [-8, -3, 2, 7, 12], [-9, -4, 1, 6, 11]]
        },
        "output": [-10, -9, -8, -5, -4, -3, 0, 1, 2, 5, 6, 7, 10, 11, 12]
    },
    "test_case_15": {
        "level": 2,
        "inputs": {
            "lists": [[100, 200, 300], [50, 150, 250], [25, 75, 125]]
        },
        "output": [25, 50, 75, 100, 125, 150, 200, 250, 300]
    },
    "test_case_16": {
        "level": 3,
        "inputs": {
            "lists": [[1] * 500, [2] * 500, [3] * 500, [4] * 500]
        },
        "output": [1] * 500 + [2] * 500 + [3] * 500 + [4] * 500
    },
    "test_case_17": {
        "level": 3,
        "inputs": {
            "lists": [[i for i in range(500)], [j for j in range(500, 1000)]]
        },
        "output": [i for i in range(1000)]
    },
    "test_case_18": {
        "level": 3,
        "inputs": {
            "lists": [[-10000, -5000, 0, 5000, 10000], [-7500, -2500, 2500, 7500]]
        },
        "output": [-10000, -7500, -5000, -2500, 0, 2500, 5000, 7500, 10000]
    },
    "test_case_19": {
        "level": 3,
        "inputs": {
            "lists": [[100, 200, 300], [50, 150, 250], [25, 75, 125], [400, 500, 600]]
        },
        "output": [25, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600]
    },
    "test_case_20": {
        "level": 3,
        "inputs": {
            "lists": [[10**4] * 500, [10**3] * 500, [10**2] * 500, [10**1] * 500]
        },
        "output": [10] * 500 + [100] * 500 + [1000] * 500 + [10000] * 500
    }
}



# Function to run tests and measure performance
def run_tests():
    solution = Solution()
    results = {}

    for test_name, test in test_cases.items():
       
        inputs = test["inputs"]["lists"]
        inputss = []
        for i in inputs:
            inputss.append(list_to_linked_list(i))
     

        exc_time =  []
        memory = []
        # Start memory and time tracking
        
        for i in range(10):
            tracemalloc.start()
            start_time = time.time()

            # Run the function
            actual_output = solution.mergeKLists(inputss)

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
                "list": inputs,
            },
            "output": linked_list_to_list(actual_output),
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
with open("testcases_generated/merge_k_sorted_lists.json", "w") as file:
    json.dump(test_results, file, indent=4)

print("\n✅ Test results saved in testcases_generated!")
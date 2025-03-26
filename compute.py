import time
import random
import json
import tracemalloc
from typing import List, Optional
from collections import deque
import math
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

class Solution:
    def recoverFromPreorder(self, traversal: str) -> Optional[TreeNode]:
        nodes = [(len(node[1]), int(node[2])) for node in re.findall("((-*)(\d+))", traversal)][::-1]
        def makeTree(depth): 
            if not nodes or depth != nodes[-1][0]: return None 
            node = TreeNode(nodes.pop()[1])
            node.left = makeTree(depth + 1) 
            node.right = makeTree(depth + 1)
            return node
        return makeTree(0) 
      
# Define test cases
test_cases = {
    "test_case_1": {
        "level": 0,
       "inputs": {"traversal" :"1"},
        "output": [1]
    },
    "test_case_2": {
        "level": 0,
        "inputs": {"traversal" :"1-2"},
        "output": [1, 2]
    },
    "test_case_3": {
        "level": 0,
        "inputs": {"traversal" :"1-2--3"},
        "output": [1, 2, None, 3]
    },
    "test_case_4": {
        "level": 0,
        "inputs": {"traversal" :"1-2--3--4"},
        "output": [1, 2, None, 3, 4]
    },
    "test_case_5": {
        "level": 0,
        "inputs": {"traversal" :"1-2--3-4--5"},
        "output": [1, 2, 4, 3, 5]
    },
    "test_case_6": {
        "level": 1,
        "inputs": {"traversal" :"1-2--3--4-5--6--7"},
        "output": [1, 2, 5, 3, 4, 6, 7]
    },
    "test_case_7": {
        "level": 1,
        "inputs": {"traversal" :"1-2--3---4-5--6---7"},
        "output": [1, 2, 5, 3, None, 6, None, 4, None, 7]
    },
    "test_case_8": {
        "level": 1,
        "inputs": {"traversal" :"1-401--349---90--88"},
        "output": [1, 401, None, 349, 88, 90]
    },
    "test_case_9": {
        "level": 1,
        "inputs": {"traversal" :"1-2--3-4--5-6--7"},
        "output": [1, 2, 4, 3, 5, 6, 7]
    },
    "test_case_10": {
        "level": 1,
        "inputs": {"traversal" :"1-2--3---4----5-6--7---8----9"},
        "output": [1, 2, 6, 3, 7, 4, 8, 5, 9]
    },
    
    "test_case_11": {
        "level": 2,
        "inputs": {"traversal" :"1" + "".join([f"-{i}" for i in range(2, 701)])},
        "output": "Binary tree with 700 nodes in a deep left chain"
    },
    "test_case_12": {
        "level": 2,
        "inputs": {"traversal" :"1-2--3-4--5" + "".join([f"-{i}" for i in range(6, 601)])},
        "output": "Binary tree with 600 nodes, mixed nesting"
    },
    "test_case_13": {
        "level": 2,
        "inputs": {"traversal" :"1" + "".join([f"-{i}" for i in range(2, 550)])},
        "output": "Binary tree with 550 nodes in a deep left chain"
    },
    "test_case_14": {
        "level": 2,
        "inputs": {"traversal" :"1-2--3--4-5--6--7" + "".join([f"-{i}" for i in range(8, 500)])},
        "output": "Binary tree with 500 nodes, alternating left-right nesting"
    },
    "test_case_15": {
        "level": 2,
        "inputs": {"traversal" :"1-2--3---4----5---6--7---8" + "".join([f"-{i}" for i in range(9, 550)])},
        "output": "Binary tree with 550 nodes, deep mixed nesting"
    },
    "test_case_16": {
        "level": 3,
        "inputs": {"traversal" :"1" + "".join([f"-{i}" for i in range(2, 1001)])},
        "output": "Binary tree with 1000 nodes in a deep left chain"
    },
    "test_case_17": {
        "level": 3,
        "inputs": {"traversal" :"1-2--3-4--5-6--7" + "".join([f"-{i}" for i in range(8, 980)])},
        "output": "Binary tree with 980 nodes, mixed nesting"
    },
    "test_case_18": {
        "level": 3,
        "inputs": {"traversal" :"1-2--3---4----5---6--7---8" + "".join([f"-{i}" for i in range(9, 960)])},
        "output": "Binary tree with 960 nodes, deep mixed nesting"
    },
    "test_case_19": {
        "level": 3,
        "inputs": {"traversal" :"1" + "".join([f"-{i}" for i in range(2, 940)])},
        "output": "Binary tree with 940 nodes in a deep left chain"
    },
    "test_case_20": {
        "level": 3,
        "inputs": {"traversal" :"1-2--3---4----5---6--7---8" + "".join([f"-{i}" for i in range(9, 920)])},
        "output": "Binary tree with 920 nodes, deep mixed nesting"
    }
}



# Function to run tests and measure performance
def run_tests():
    solution = Solution()
    results = {}

    for test_name, test in test_cases.items():
       
        traversal = test["inputs"]["traversal"]


        exc_time =  []
        memory = []
        # Start memory and time tracking
        
        for i in range(10):
            tracemalloc.start()
            start_time = time.time()

            # Run the function
            actual_output = solution.recoverFromPreorder(traversal=traversal)

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
                "traversal" : traversal

            },
            "output": tree_to_list(actual_output),
            "excecution_time" : avg_time * 1000 ,
            "memory_used" : peak / 1024
        }

        # Print results to console
        print(f"Test: {test_name}")
        print(f"  Expected Output: {test['output']}")
        print(f"  Actual Output: {actual_output}")
        print(f"  Passed: {tree_to_list(actual_output) == test['output']}")
        print(f"  Execution Time: {avg_time * 1000} ms")
        print(f"  Memory Used: {round(peak / 1024, 4)} KB")
        print("-" * 50)

    return results

# Run the tests and collect results
test_results = run_tests()

# Save results to a JSON file
with open("testcases_generated/recover_a_tree_from_preorder_traversal.json", "w") as file:
    json.dump(test_results, file, indent=4)

print("\n✅ Test results saved in testcases_generated!")
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
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        # Initialize the array to hold the right side view elements
        right_side_view = []
      
        # If the tree is empty, return the empty list
        if root is None:
            return right_side_view
      
        # Use deque as a queue to hold the nodes at each level
        queue = deque([root])
      
        # Continue until the queue is empty
        while queue:
            # The rightmost element at the current level is visible from the right side
            right_side_view.append(queue[-1].val)
          
            # Iterate over nodes at the current level
            for _ in range(len(queue)):
                # Pop the node from the left side of the queue
                current_node = queue.popleft()
              
                # If left child exists, add it to the queue
                if current_node.left:
                    queue.append(current_node.left)
              
                # If right child exists, add it to the queue
                if current_node.right:
                    queue.append(current_node.right)
                  
        # Return the list containing the right side view of the tree
        return right_side_view

# Define test cases
test_cases = {
    # Level 0: Basic Correctness & Edge Cases (5 test cases)
    "test_case_1": {
        "inputs": {
            "root": [1,2,3,None,5,None,4]
        },
        "output": [1,3,4]  # Rightmost nodes from top to bottom
    },
    "test_case_2": {
        "inputs": {
            "root": [1,2,3,4,None,None,None,5]
        },
        "output": [1,3,4,5]  # Rightmost path down
    },
    "test_case_3": {
        "inputs": {
            "root": [1,None,3]
        },
        "output": [1,3]  # Right-skewed tree
    },
    "test_case_4": {
        "inputs": {
            "root": []
        },
        "output": []  # Empty tree case
    },
    "test_case_5": {
        "inputs": {
            "root": [1]
        },
        "output": [1]  # Single node tree
    },

    # Level 1: Moderate Cases (5 test cases)
    "test_case_6": {
        "inputs": {
            "root": [1,2,3,4,5,6,7]
        },
        "output": [1,3,7]  # Complete tree with clear right-side nodes
    },
    "test_case_7": {
        "inputs": {
            "root": [10,8,15,6,9,12,20,None,7,None,None,11,13,18,25]
        },
        "output": [10,15,20,25]  # Rightmost visible nodes
    },
    "test_case_8": {
        "inputs": {
            "root": [5,3,10,None,4,None,12]
        },
        "output": [5,10,12]  # Unbalanced tree, right-skewed
    },
    "test_case_9": {
        "inputs": {
            "root": [7,3,8,2,5,None,10,1,None,4,6,None,None,9,12]
        },
        "output": [7,8,10,12]  # Right nodes from top to bottom
    },
    "test_case_10": {
        "inputs": {
            "root": [1,2,3,None,5,None,4,None,None,6]
        },
        "output": [1,3,4,6]  # Zig-zag tree with clear right view
    },

    # Level 2: Larger Trees (5 test cases)
    "test_case_11": {
        "inputs": {
            "root": [i for i in range(1, 32)]  # Full binary tree (1-31)
        },
        "output": [1,3,7,15,31]  # Rightmost nodes at each level
    },
    "test_case_12": {
        "inputs": {
            "root": [20,10,30,5,15,25,35,None,7,12,18,22,28,33,40]
        },
        "output": [20,30,35,40]  # Rightmost nodes in a balanced tree
    },
    "test_case_13": {
        "inputs": {
            "root": [50,30,70,20,40,60,80,None,None,None,45,None,65,None,85]
        },
        "output": [50,70,80,85]  # Unbalanced binary tree
    },
    "test_case_14": {
        "inputs": {
            "root": [i for i in range(1, 40, 2)]  # Sparse right-leaning tree
        },
        "output": [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39]  # All rightmost nodes
    },
    "test_case_15": {
        "inputs": {
            "root": [100,-10,200,-20,50,150,250,None,-15,45,None,None,175,None,300]
        },
        "output": [100,200,250,300]  # Complex tree with deep right side
    },

    # Level 3: Stress Tests (5 test cases)
    "test_case_16": {
        "inputs": {
            "root": [i for i in range(1, 101)]  # Full tree with 100 nodes
        },
        "output": [1,3,7,15,31,63,100]  # Deepest rightmost visible nodes
    },
    "test_case_17": {
        "inputs": {
            "root": [i for i in range(1, 101) if i % 2 == 0]  # Even values, right-skewed
        },
        "output": [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100]  # All right nodes
    },
    "test_case_18": {
        "inputs": {
            "root": [1] + [None] * 99  # A single deep rightmost path
        },
        "output": [1]  # Only root is visible
    },
    "test_case_19": {
        "inputs": {
            "root": [100] + [i for i in range(99, 0, -1)]  # Left-heavy tree
        },
        "output": [100]  # Only root is visible
    },
    "test_case_20": {
        "inputs": {
            "root": [100, 50, 150, 25, 75, 125, 175, 12, 37, 63, 87, 112, 138, 162, 188] + [i for i in range(189, 250)]
        },
        "output": [100,150,175,188,249]  # Rightmost visible nodes in a large, deep tree
    }
}

# Function to run tests and measure performance
def run_tests():
    solution = Solution()
    results = {}

    for test_name, test in test_cases.items():
       
        root = test["inputs"]["root"]
     

        exc_time =  []
        memory = []
        # Start memory and time tracking
        
        for i in range(10):
            tracemalloc.start()
            start_time = time.time()

            # Run the function
            actual_output = solution.rightSideView(list_to_tree(root))

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
            "inputs": {
                "root" : root, 
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
with open("testcases_generated/binary_tree_right_side_view.json", "w") as file:
    json.dump(test_results, file, indent=4)

print("\n✅ Test results saved to 'test_results.json'!")
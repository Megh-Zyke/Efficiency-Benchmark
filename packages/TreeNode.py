from typing import Optional, List
from collections import deque

# Definition of TreeNode
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Function to convert a list into a binary tree
def list_to_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None  # Empty tree case

    root = TreeNode(values[0])  # Create root node
    queue = deque([root])
    i = 1  # Index to track position in `values`

    while queue and i < len(values):
        node = queue.popleft()  # Get the current node

        # Process left child
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        # Process right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root  # Return the constructed tree

# Function to convert a binary tree back to a list
def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    if not root:
        return []  # Handle empty tree

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)  # Store node value
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)  # Mark missing nodes as None

    # Trim trailing `None` values to match compact list format
    while result and result[-1] is None:
        result.pop()

    return result

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def build_graph(adjList):
    if not adjList:
        return None  # Handle empty graph case

    # Step 1: Create a dictionary to store nodes by value
    node_map = {i + 1: Node(i + 1) for i in range(len(adjList))}

    # Step 2: Connect each node to its neighbors
    for i, neighbors in enumerate(adjList):
        node_map[i + 1].neighbors = [node_map[neighbor] for neighbor in neighbors]

    return node_map[1] 

def graph_to_adj_list(node):
    if not node:
        return []

    visited = {}
    adjList = {}

    def dfs(n):
        if n.val in visited:
            return
        visited[n.val] = n
        adjList[n.val] = [neighbor.val for neighbor in n.neighbors]
        for neighbor in n.neighbors:
            dfs(neighbor)

    dfs(node)

    # Convert dictionary to list format (1-indexed)
    max_index = max(adjList.keys())
    return [adjList.get(i, []) for i in range(1, max_index + 1)]
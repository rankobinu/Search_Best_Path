from collections import deque
import time

def find_shortest_path_bfs(G, start, goal):
    start_time = time.perf_counter()
    queue = deque([start])
    meta = {start: [None, 0]}
    expanded_nodes = [] # Changed to list
    
    while queue:
        curr = queue.popleft()
        expanded_nodes.append(curr) # Record the expanded node
        
        if curr == goal:
            break
            
        for neighbor in G.neighbors(curr):
            if neighbor not in meta:
                meta[neighbor] = [curr, meta[curr][1] + 1]
                queue.append(neighbor)
                
    if curr != goal:
        return None, float('inf'), expanded_nodes, time.perf_counter() - start_time
        
    path = []
    curr_trace = goal
    while curr_trace is not None:
        path.append(curr_trace)
        curr_trace = meta[curr_trace][0]
        
    execution_time = time.perf_counter() - start_time
    return path[::-1], meta[goal][1], expanded_nodes, execution_time
import heapq
import time

def find_shortest_path_ucs(G, start, goal):
    start_time = time.perf_counter()
    queue = [(0, start)]
    meta = {start: [None, 0]}
    expanded_nodes = [] # Changed to list
    
    while queue:
        curr_cost, curr = heapq.heappop(queue)
        expanded_nodes.append(curr) # Record the expanded node
        
        if curr == goal:
            break
            
        for neighbor in G.neighbors(curr):
            edge_data = G.get_edge_data(curr, neighbor)
            weight = edge_data[0].get('length', 1.0)
            new_cost = meta[curr][1] + weight
            
            if neighbor not in meta or new_cost < meta[neighbor][1]:
                meta[neighbor] = [curr, new_cost]
                heapq.heappush(queue, (new_cost, neighbor))
                
    if curr != goal:
        return None, float('inf'), expanded_nodes, time.perf_counter() - start_time
        
    path = []
    curr_trace = goal
    while curr_trace is not None:
        path.append(curr_trace)
        curr_trace = meta[curr_trace][0]
        
    execution_time = time.perf_counter() - start_time
    return path[::-1], meta[goal][1], expanded_nodes, execution_time
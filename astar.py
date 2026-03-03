import heapq
import time
import math

def euclidean_distance_meters(y1, x1, y2, x2):
    degree_dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return degree_dist * 111139.0

def find_shortest_path_astar(G, start, goal):
    start_time = time.perf_counter()
    goal_y, goal_x = G.nodes[goal]['y'], G.nodes[goal]['x']
    
    queue = [(0, start)]
    meta = {start: [None, 0]}
    expanded_nodes = [] # Changed to list
    
    while queue:
        curr_f, curr = heapq.heappop(queue)
        expanded_nodes.append(curr) # Record the expanded node
        
        if curr == goal:
            break
            
        curr_g = meta[curr][1]
            
        for neighbor in G.neighbors(curr):
            edge_data = G.get_edge_data(curr, neighbor)
            weight = edge_data[0].get('length', 1.0)
            new_g = curr_g + weight
            
            if neighbor not in meta or new_g < meta[neighbor][1]:
                n_y, n_x = G.nodes[neighbor]['y'], G.nodes[neighbor]['x']
                h_n = euclidean_distance_meters(n_y, n_x, goal_y, goal_x)
                f_n = new_g + h_n
                
                meta[neighbor] = [curr, new_g]
                heapq.heappush(queue, (f_n, neighbor))
                
    if curr != goal:
        return None, float('inf'), expanded_nodes, time.perf_counter() - start_time
        
    path = []
    curr_trace = goal
    while curr_trace is not None:
        path.append(curr_trace)
        curr_trace = meta[curr_trace][0]
        
    execution_time = time.perf_counter() - start_time
    return path[::-1], meta[goal][1], expanded_nodes, execution_time
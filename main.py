import osmnx as ox
import matplotlib.pyplot as plt
from bfs import find_shortest_path_bfs as bfs
from ucs import find_shortest_path_ucs as ucs
from astar import find_shortest_path_astar as astar

def render_algorithm_map(G, path, expanded_nodes, start_node, goal_node, algo_name):
    """Helper function to plot the graph, expanded nodes, and path."""
    print(f"Rendering {algo_name} map...")
    
    # 1. Base map and shortest path [cite: 92, 95]
    fig, ax = ox.plot_graph_route(
        G, 
        path, 
        route_color='blue', 
        route_linewidth=3, 
        node_size=0, 
        bgcolor='white', 
        show=False, 
        close=False
    )
    
    # 2. Extract coordinates for EXPANDED nodes and plot them (Orange)
    exp_x = [G.nodes[n]['x'] for n in expanded_nodes]
    exp_y = [G.nodes[n]['y'] for n in expanded_nodes]
    ax.scatter(exp_x, exp_y, c='orange', s=15, alpha=0.6, label='Expanded', zorder=2)

    # 3. Extract coordinates for Start/Goal and plot them [cite: 89, 91]
    start_y, start_x = G.nodes[start_node]['y'], G.nodes[start_node]['x']
    goal_y, goal_x = G.nodes[goal_node]['y'], G.nodes[goal_node]['x']
    ax.scatter(start_x, start_y, c='green', s=100, label='Start', zorder=5)
    ax.scatter(goal_x, goal_y, c='red', s=100, label='Goal', zorder=5)

    # Add title and save [cite: 93]
    plt.title(f"{algo_name} Search (Expanded: {len(expanded_nodes)} nodes)")
    filename = f"{algo_name.lower()}_blida_path.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved {filename}!\n")
    plt.close(fig) # Close the figure to free up memory

def main():
    print("Downloading map data... (This may take a minute)")
    place = "Blida, Algeria" 
    G = ox.graph_from_place(place, network_type="drive")
    G = ox.distance.add_edge_lengths(G)
    print(f"Map downloaded! Total nodes: {len(G.nodes)}\n")

    start_coords = ox.geocode("Blida, Algeria")
    goal_coords = ox.geocode("Beni Mered, Blida, Algeria")

    start_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
    goal_node = ox.distance.nearest_nodes(G, goal_coords[1], goal_coords[0])

    print("--- Running BFS ---")
    path_bfs, cost_bfs, exp_bfs, time_bfs = bfs(G, start_node, goal_node)
    print(f"BFS Expanded Nodes: {len(exp_bfs)}")
    print(f"BFS Time (s): {time_bfs:.4f}\n")

    print("--- Running UCS ---")
    path_ucs, cost_ucs, exp_ucs, time_ucs = ucs(G, start_node, goal_node)
    print(f"UCS Path Length (m): {cost_ucs:.2f}")
    print(f"UCS Expanded Nodes: {len(exp_ucs)}")
    print(f"UCS Time (s): {time_ucs:.4f}\n")
    
    print("--- Running A* ---")
    path_astar, cost_astar, exp_astar, time_astar = astar(G, start_node, goal_node)
    print(f"A* Path Length (m): {cost_astar:.2f}")
    print(f"A* Expanded Nodes: {len(exp_astar)}")
    print(f"A* Time (s): {time_astar:.4f}\n")

    # Visualizations
    if path_bfs: render_algorithm_map(G, path_bfs, exp_bfs, start_node, goal_node, "BFS")
    if path_ucs: render_algorithm_map(G, path_ucs, exp_ucs, start_node, goal_node, "UCS")
    if path_astar: render_algorithm_map(G, path_astar, exp_astar, start_node, goal_node, "AStar")

if __name__ == "__main__":
    main()
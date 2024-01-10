import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adjacency_list = {vertex: [] for vertex in vertices}

    def add_edge(self, u, v):
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)

    def is_bipartite(self):
        colors = {vertex: 0 for vertex in self.vertices}  # 0: Not colored, 1 and 2 for different colors
        queue = deque()

        for vertex in self.vertices:
            if colors[vertex] == 0:
                queue.append(vertex)
                colors[vertex] = 1  # Color vertex 1 initially
                while queue:
                    current = queue.popleft()
                    for neighbor in self.adjacency_list[current]:
                        if colors[neighbor] == 0:
                            colors[neighbor] = 3 - colors[current]  # Assign opposite color
                            queue.append(neighbor)
                        elif colors[neighbor] == colors[current]:
                            return False  # Not bipartite if adjacent nodes have same color
        return colors  # Return colors after bipartite check

# Function to color vertices based on bipartite sets
def color_vertices(G, colors):
    bipartite_sets = [{node for node, color in colors.items() if color == 1},
                      {node for node, color in colors.items() if color == 2}]
    colors = ['red' if node in bipartite_sets[0] else 'blue' for node in G.nodes()]
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, font_weight='bold')
    plt.show()

# Input vertices and edges
vertices = input("Enter vertices (separated by space): ").split()
edges = []
while True:
    edge_input = input("Enter edge as 'vertex1 vertex2' (or 'done' to finish): ")
    if edge_input.lower() == 'done':
        break
    else:
        edge = tuple(edge_input.split())
        if len(edge) == 2 and all(v in vertices for v in edge):
            edges.append(edge)
        else:
            print("Invalid input. Please enter two valid vertices.")

# Create graph
graph = Graph(vertices)
for edge in edges:
    graph.add_edge(*edge)

# Check if the graph is bipartite and plot visualization or show without button
is_bipartite = graph.is_bipartite()
if is_bipartite:
    print("The graph is Bipartite.")
    root = tk.Tk()
    root.title("Graph Visualization")
    fig, ax = plt.subplots(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Function to execute when the button is pressed
    def on_button_click():
        colors = graph.is_bipartite()
        color_vertices(G, colors)  # Call the function to color vertices based on bipartite sets

    # Create a button
    button = tk.Button(root, text="Color Vertices", command=on_button_click, font=("Arial", 16), bg="brown", fg="white")
    canvas.get_tk_widget().create_window(10, 10, anchor=tk.NW, window=button)

    # Display the graph in tkinter window
    G = nx.Graph()
    G.add_nodes_from(graph.vertices)
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, font_weight='bold')
    plt.close()  # Close the initial plot
    canvas.draw()
    button.pack(side=tk.BOTTOM) # Pack the button at the bottom
    tk.mainloop()

else:
    print("The graph is Not Bipartite. Displaying without coloring.")
    G = nx.Graph()
    G.add_nodes_from(graph.vertices)
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, font_weight='bold')
    plt.show()

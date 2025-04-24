import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos
G.add_nodes_from(["Madrid", "Barcelona", "Valencia", "Sevilla", "Granada", "Bilbao"])

# Agregar aristas con pesos
G.add_weighted_edges_from([
    ("Madrid", "Barcelona", 620),
    ("Madrid", "Valencia", 350),
    ("Madrid", "Sevilla", 510),
    ("Barcelona", "Valencia", 350),
    ("Valencia", "Sevilla", 550),
    ("Sevilla", "Granada", 120),
    ("Granada", "Bilbao", 700)
])

# Visualizar el grafo con pesos
pos = nx.spring_layout(G)  # Posiciones para los nodos
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, font_size=10)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()

# Calcular el camino más corto
camino_mas_corto = nx.dijkstra_path(G, "Madrid", "Granada", weight="weight")
print("Camino más corto de Madrid a Granada:", camino_mas_corto)

# Eliminar Valencia y sus aristas
G.remove_node("Valencia")

# Visualizar el grafo modificado
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=1500, font_size=10)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()

# Intentar calcular el camino más corto nuevamente
try:
    camino_mas_corto = nx.dijkstra_path(G, "Madrid", "Granada", weight="weight")
    print("Camino más corto de Madrid a Granada (después de eliminar Valencia):", camino_mas_corto)
except nx.NetworkXNoPath:
    print("No existe camino de Madrid a Granada después de eliminar Valencia.")
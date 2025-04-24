from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from matplotlib.offsetbox import OffsetImage, AnnotationBbox #Importamos AnnotationBbox

# Cargar la imagen de la bandera (JPG)
bandera_path = "bandera_cochabamba.jpg"
bandera_img = Image.open(bandera_path).convert("RGB")

# Redimensionar la imagen a un cuadrado (ejemplo: 200x200)
tamaño = 600
bandera_img = bandera_img.resize((tamaño, tamaño))

# Crear una máscara circular
mask = Image.new("L", bandera_img.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, bandera_img.size[0], bandera_img.size[1]), fill=255)

# Aplicar la máscara a la imagen de la bandera
bandera_circular = Image.new("RGBA", bandera_img.size)
bandera_circular.paste(bandera_img, mask=mask)

# Crear un grafo no dirigido
G = nx.Graph()

# Agregar nodos (intersecciones y puntos de referencia)
nodos = [
    "Av. Oquendo esq. Calle Jordán",
    "Calle Jordán esq. Calle Lanza",
    "Calle Lanza esq. Calle Ecuador",
    "Plaza Colón",
    "Calle Mayor Rocha esq. Calle Ecuador"
]
G.add_nodes_from(nodos)

# Agregar aristas (calles) con pesos (distancias estimadas)
G.add_weighted_edges_from([
    ("Av. Oquendo esq. Calle Jordán", "Calle Jordán esq. Calle Lanza", 300),
    ("Calle Jordán esq. Calle Lanza", "Calle Lanza esq. Calle Ecuador", 250),
    ("Calle Lanza esq. Calle Ecuador", "Calle Mayor Rocha esq. Calle Ecuador", 200),
    ("Calle Mayor Rocha esq. Calle Ecuador", "Plaza Colón", 350)
])

# Visualizar el grafo con imágenes de la bandera circular
pos = nx.spring_layout(G)
fig, ax = plt.subplots()
nx.draw_networkx_edges(G, pos, ax=ax)

# Agregar imágenes de la bandera circular a los nodos
for nodo in nodos:
    ab = AnnotationBbox(OffsetImage(bandera_circular, zoom=0.1), pos[nodo], frameon=False)
    ax.add_artist(ab)

# Agregar etiquetas de texto a los nodos
nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)

# Agregar etiquetas de peso a las aristas
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

plt.show()
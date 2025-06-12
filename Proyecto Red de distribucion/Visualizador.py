import networkx as nx
import matplotlib.pyplot as plt

def visualizar_red(grafo, atributos, fallas_nodos=None, fallas_conex=None, sugerencias=None):

    G = nx.Graph()
    fallas_nodos = fallas_nodos or set()
    fallas_conex  = fallas_conex  or set()
    sugerencias   = sugerencias   or []

    #tamaño de la figura
    plt.figure(figsize=(12, 12))

    # Agrega nodos con su color segun tipo o estado
    for nodo, attrs in atributos.items():
        tipo = attrs.get("tipo", "")
        if nodo in fallas_nodos:
            color = "red"
        elif tipo.startswith("subestacion") or tipo.startswith("central"):
            color = "green"
        elif tipo.startswith("transformador"):
            color = "orange"
        elif tipo.startswith("poste"):
            color = "skyblue"
        else:
            color = "yellow"
        G.add_node(nodo, color=color)

    # Agrega aristas con estilo segun esten caidas o no
    for u, vecinos in grafo.items():
        for (v, distancia) in vecinos:
            if not G.has_edge(u, v):
                falla = frozenset((u, v)) in fallas_conex
                estilo = "dashed" if falla else "solid"
                col = "red" if falla else "black"
                G.add_edge(u, v, style=estilo, color=col, weight=distancia)

    try:
        pos = nx.kamada_kawai_layout(G)
    except Exception:
        pos = nx.spring_layout(G, k=1.2, iterations=100)

    # Dibuja nodos
    colores_nodos = [data["color"] for _, data in G.nodes(data=True)]
    nx.draw_networkx_nodes(G, pos, node_color=colores_nodos, node_size=700)

    # Dibuja todas las aristas (rojo punteado para fallas, negro solido para normales)
    estilos   = [G[u][v]["style"] for u, v in G.edges()]
    colores_are = [G[u][v]["color"] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos,
                           style=estilos,
                           edge_color=colores_are,
                           width=2)

    #Dibujaa en verde las aristas de las rutas sugeridas
    if sugerencias:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=sugerencias,
            edge_color="green",
            width=4
        )

    # tamaño de las etiquetas
    etiquetas_desplazadas = {}
    for nodo, (x, y) in pos.items():
        etiquetas_desplazadas[nodo] = (x + 0.05, y + 0.05)

    nx.draw_networkx_labels(G, etiquetas_desplazadas, font_size=11)

    plt.title("Red de Distribución", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


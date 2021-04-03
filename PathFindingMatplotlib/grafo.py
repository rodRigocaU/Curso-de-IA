
import networkx as nx
import matplotlib.pyplot as plt


def create_graph():

    row = int(input("Ingrese el numero de Filas: "))
    column = int(input("Ingrese el numero de Filas: "))

    G = nx.Graph()

    i = 1

    # Ejes
    x = 1
    y = 1

    while i <= row * column:
        G.add_node(i, sign=i, eje_x=x, eje_y=y)
        x+=1

        if i % column == 0:
            y -= 1
            x = 1

        i += 1

    # Crear aristas
    list_nodes = list(G.nodes)
    j = 0

    index_row = 1

    while j < len(list_nodes):

        # Si eres el elemento final de la fila
        if not list_nodes[j] % column:
            # Indice no este entre el rango de la ultima fila
            if j < (row * column) - column:
                # Conectar Abajo
                G.add_edge(list_nodes[j], list_nodes[j + column], peso = 1 )
                # Conectar diagonal abajo derecha
                G.add_edge(list_nodes[j], list_nodes[j + column - 1],peso = 1)
            j += 1

            index_row += 1

        else:
            # Conectar vecino derecho
            G.add_edge(list_nodes[j], list_nodes[j + 1],peso = 1)

            # Si no perteneces a la ultima fila
            if j < ((row - 1) * column):
                # Conectar Abajo
                G.add_edge(list_nodes[j], list_nodes[j + column],peso = 1)

                # Conectar diagonal abajo derecha \
                G.add_edge(list_nodes[j], list_nodes[j + column+1],peso = 1)

                # Si no eres primer elemento de la fila
                if j != (index_row - 1) * column:
                    # Diagonal abajo izquierda
                    G.add_edge(list_nodes[j], list_nodes[j + column - 1],peso = 1)

            j += 1
    return G


# Dibuja el grafo sinmple sin colorear
def draw_graph_mat(G):
    pos = nx.spring_layout(G)
    # nx.draw_networkx(G, pos)
    nx.draw_networkx(G, pos)
    plt.grid()
    plt.pause(1)
    plt.show()



def Colored_edges(G, path):
    edge_colors = []
    for i in range(len(G.edges)):
        edge_colors.append("black")

    list_id = []
    for signo in path:
        list_id.append(signo)

    indice = 0
    for id in range(len(list_id) - 1):

        for indice, edge in enumerate(G.edges):
            if (edge[0] == list_id[id] and edge[1] == list_id[id + 1]) or (
                    edge[1] == list_id[id] and edge[0] == list_id[id + 1]):
                edge_colors[indice] = "blue"
    return edge_colors


# Colorea el camino dado y dibuja el grafo
def draw_color_graph_mat(G, path):
    if path:
        edge_colors = Colored_edges(G, path)
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, edge_color=edge_colors)
        plt.grid()
        # plt.show()
    else:
        draw_graph_mat(G)



# No retornamos nada porque G es pasado por referencia
def remove_nodo(G, idNodo):
    # Remover un nodo solo pasamos el id del nodo
    try:
        # Se elimina el nodo y sus aristas adyacentes
        G.remove_node(idNodo)
    # El error de si no encuentra el nodo es keyerror y networkx.exception.NetworkXError
    except nx.exception.NetworkXError:
        print("No existe el nodo que escogiste para eliminar seleccionado")



import networkx as nx
import matplotlib.pyplot as plt

# Grafo de malla interconectado en cruz y conexion de derecha,abajo
def create_graph():

    row = int(input("Ingrese el numero de Filas: "))
    column = int(input("Ingrese el numero de Filas: "))

    # Funcion pero falta una arista para pasar
    # row = 5
    # column = 4

    # Funciona Bien
    # row = 5
    # column = 3

    # row = 5
    # column = 6

    # row = 10
    # column = 7

    # Con lag
    # row = 20
    # column = 20

    # row = 30
    # column = 30

    G = nx.Graph()

    # Rellenar Nodos
    i = 1

    # Ejes
    x = 1
    y = 1

    while i <= row * column:

        # print(x,y)

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
            # if j != (row * column) - 1:
            if j < (row * column) - column:
                # Conectar Abajo
                # G.add_edge(list_nodes[j], list_nodes[j + row - 1])
                G.add_edge(list_nodes[j], list_nodes[j + column], peso = 1 )

                # Conectar diagonal abajo derecha /
                G.add_edge(list_nodes[j], list_nodes[j + column - 1],peso = 1)

            j += 1

            index_row += 1

        # Elementso que no pertenecen al ultimo elemento de la fila
        else:
            # Conectar vecino derecho
            G.add_edge(list_nodes[j], list_nodes[j + 1],peso = 1)

            # Condicion de que se puede conectar con el de abajo
            # entra si el indice no pertence a la ultima fila y por el primer if no ser ultimo elemento de la fila
            if j < ((row - 1) * column):
                # Conectar Abajo
                # G.add_edge(list_nodes[j], list_nodes[j + row - 1])
                G.add_edge(list_nodes[j], list_nodes[j + column],peso = 1)

                # Conectar diagonal abajo derecha \
                # G.add_edge(list_nodes[j], list_nodes[j + row])
                G.add_edge(list_nodes[j], list_nodes[j + column+1],peso = 1)

                # Pregunta si no eres el elemento el primer elemnto de la fila
                if j != (index_row - 1) * column:
                    G.add_edge(list_nodes[j], list_nodes[j + column - 1],peso = 1)

            # print((column*index_row)-1)

            j += 1

    # https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.degree.html?highlight=degree#networkx.classes.function.degree
    # Saber el grado de los nodos, nos devuelve una lista con el (id,grado)
    # print(nx.degree(G))
    # draw_graph_mat(G)

    return G


# Grafo S ,A B,D,E,F,G
def test_graph():
    G = nx.Graph()
    G.add_nodes_from([
        (1, {"char": "S"}),
        (2, {"char": "A"}),
        (3, {"char": "D"}),
        (4, {"char": "B"}),
        (5, {"char": "E"}),
        (6, {"char": "C"}),
        (7, {"char": "F"}),
        (8, {"char": "G"})

        # Comprobar que recorre por todo al insertar un nodo sin conxeiones
        # ,(9, {"char": "H"})
    ])

    # list_edges=[('S','A'),('S','D'),('A','D'),('A','B'),('B','E'),('D','E'),('B','C'),('E','F'),('F','G')]
    # list_edges = [(1, 2), (1, 3), (2, 3), (2, 4), (4, 5), (3, 5), (4, 6), (5, 7),(7, 8)]
    list_edges = [(1, 2), (1, 3), (2, 4), (2, 3), (4, 5), (3, 5), (4, 6), (5, 7), (7, 8)]
    G.add_edges_from(list_edges)

    # Obtener nodos que tiene el atributo que ponga en el segundo parametro
    # print(nx.get_node_attributes(G,'char'))

    # Imprime el nodo con todo sus atrubutos
    # print(G.nodes[1])

    # draw_graph_mat(G)

    # Dibujar con color a todo los nodos en azul
    # nx.draw(G,node_color='blue',with_labels=True)
    # plt.show()
    return G


# Dibuja el grafo sinmple sin colorear
def draw_graph_mat(G):
    pos = nx.spring_layout(G)
    # nx.draw_networkx(G, pos)
    nx.draw_networkx(G, pos)
    plt.grid()
    plt.pause(1)
    plt.show()



# Colorear aristas y dibujar el grafo
def colored_edges(G, path):
    edge_colors = []
    for i in range(len(G.edges)):
        edge_colors.append("black")

    list_id = []
    for signo in path:
        list_id.append([x for x, y in G.nodes(data=True) if y['char'] == signo][0])

    print(list_id)

    indice = 0
    # print(len(G.edges))
    print(G.edges)

    for id in range(len(list_id) - 1):

        for indice, edge in enumerate(G.edges):

            # print("edge= ", edge[0], " ", edge[1], end="  ")
            # print("conexion a encontrar= ", list_id[id], " ", list_id[id + 1])

            if (edge[0] == list_id[id] and edge[1] == list_id[id + 1]) or (
                    edge[1] == list_id[id] and edge[0] == list_id[id + 1]):
                edge_colors[indice] = "blue"
                print(edge_colors)
                # print("edge= ", edge[0]," ",edge[1],end="  ")
                # print("conexion a encontrar= ",list_id[id], " ", list_id[id + 1])

    # print(edge_colors)
    return edge_colors


def Colored_edges(G, path):
    edge_colors = []
    for i in range(len(G.edges)):
        edge_colors.append("black")

    list_id = []
    for signo in path:
        list_id.append(signo)

    # print(list_id)

    indice = 0
    # print(len(G.edges))
    # print(G.edges)

    for id in range(len(list_id) - 1):

        for indice, edge in enumerate(G.edges):
            if (edge[0] == list_id[id] and edge[1] == list_id[id + 1]) or (
                    edge[1] == list_id[id] and edge[0] == list_id[id + 1]):
                edge_colors[indice] = "blue"
                # print(edge_colors)

    return edge_colors


# Colorea el camino dado y dibuja el grafo
def draw_color_graph_mat(G, path):
    # edge_colors = colored_edges(G,path)

    if path:
        edge_colors = Colored_edges(G, path)
        # edge_colors = colored_edges(G, path)
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


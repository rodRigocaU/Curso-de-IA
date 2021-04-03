

from grafo import *
import numpy as np
import operator



# Para el grafo de pruo numero
# DFS profundidad
def Dfs(G,sign_node_origen , sign_node_goal):
    try:
        # El filtrado deuvelve en forma de lista por eso ponemos [0] porque deberia ser unico
        # id_node_origen = [x for x, y in G.nodes(data=True) if y['char'] == sign_node_origen][0]
        # id_node_goal = [x for x, y in G.nodes(data=True) if y['char'] == sign_node_goal][0]

        id_node_origen = sign_node_origen
        id_node_goal = sign_node_goal


        L = [[G.nodes[id_node_origen]['sign']]]
        node_goal = G.nodes[id_node_goal]['sign']

    except ValueError:
        print("El nodo de origen origen o de destino escrito no existe")
        L = []
    except IndexError:
        print("El nodo de origen origen o de destino escrito no existe")
        L = []
    except KeyError:
        print("El nodo de origen origen o de destino escrito no existe")
        L = []

    # Nuestra L temporal para almcenar nuevos caminos que son posibles recorrer
    L_temp = []

    while (len(L) != 0):

        # n es el simbolo del nodo que nos enctramos
        n = L[0][0]

        if n == node_goal:
            # Retornamos todo el camino , lo invertimos porque el camino inicia con el nodo objetivo
            L[0].reverse()
            return L[0]
        else:
            signo_nodo_eliminado = n
            # print("Signo a Eliminar: ",signo_nodo_eliminado)

            id_nodo_eliminado = signo_nodo_eliminado
            # print("ID del Nodo a Eliminar: ",id_nodo_eliminado)

            # Guardamos el Camino recorrido
            path = L[0]
            L.pop(0)

            # Obtenemos la lista de los vecinos de los nodos
            list_id_vecinos = list(nx.neighbors(G, id_nodo_eliminado))
            # print("Lista de ID : ",list_id_vecinos)
            # print("Camino : ",path)

            L_temp.clear()

            for id_nbr in list_id_vecinos:
                simbolo_nuevo = G.nodes[id_nbr]['sign']

                path_nuevo = path.copy()

                # Evitar bucles en el grafo es preguntar por el camino recorrido si hay un antecente
                if not simbolo_nuevo in path_nuevo:
                    # Añadimos al camino recorrido la nueva decision es devir el simbolo correspondiente
                    path_nuevo.insert(0, simbolo_nuevo)

                    # L_temp solo almacena los caminos de los hijos que podemos avanzar, se separa porque L tiene ya Nodo aun por explorar
                    L_temp.append(path_nuevo)

            # print("Lista Nueva: ",L_temp)

            # Actualizamos la lista de L con la lista de nuevos caminos
            L = L_temp + L
            # print(L)

    else:
        print("No hay solucion")
        return None


# bfs amplitud
def Bfs(G,sign_node_origen , sign_node_goal):

    try:
        id_node_origen = sign_node_origen
        id_node_goal = sign_node_goal

        L = [[G.nodes[id_node_origen]['sign']]]
        node_goal = G.nodes[id_node_goal]['sign']

    except ValueError:
        print("El nodo de origen origen o de destino escrito no existe")
        L = []
    except IndexError:
        print("El nodo de origen origen o de destino escrito no existe")
        L = []
    except KeyError:
        print("El nodo de origen origen o de destino escrito no existe")
        L = []

    # Nuestra L temporal para almacenar nuevos caminos que son posibles recorrer
    L_temp = []

    while (len(L) != 0):
        # n es el simbolo del nodo que nos encontramos
        n = L[0][0]

        if n == node_goal:
            # Retornamos todo el camino , lo invertimos porque el camino inicia con el nodo objetivo
            L[0].reverse()
            return L[0]
        else:
            signo_nodo_eliminado = n
            id_nodo_eliminado = signo_nodo_eliminado

            # Guardamos el Camino recorrido
            path = L[0]
            L.pop(0)

            # Obtenemos la lista de los vecinos de los nodos
            list_id_vecinos = list(nx.neighbors(G, id_nodo_eliminado))

            L_temp.clear()

            for id_nbr in list_id_vecinos:
                simbolo_nuevo = G.nodes[id_nbr]['sign']

                path_nuevo = path.copy()

                # Evitar bucles en el grafo es preguntar por el camino recorrido si hay un antecente
                if not simbolo_nuevo in path_nuevo:
                    # Añadimos al camino recorrido la nueva decision es devir el simbolo correspondiente
                    path_nuevo.insert(0, simbolo_nuevo)

                    # L_temp solo almacena los caminos de los hijos que podemos avanzar, se separa porque L tiene ya Nodo aun por explorar
                    L_temp.append(path_nuevo)

            # Actualizamos la lista de L con la lista de nuevos caminos
            L = L + L_temp

    else:
        print("No hay solucion")
        return None


# Distancia euclidiana y creacion de la tabla para la heuristica
def distance_euclidean(ejes_nodo_obejtivo,ejes_nodo):
    return np.linalg.norm(ejes_nodo_obejtivo - ejes_nodo)

def table_distance(G,idNodoObjetivo):
    table = {}

    ejes_nodo_objetivo = np.array([G.nodes[idNodoObjetivo]['eje_x'], G.nodes[idNodoObjetivo]['eje_y']])
    # print(ejes_nodo_objetivo)
    ejes_nodo = np.array([0,0])

    for node in G.nodes(data=True):
        ejes_nodo[0]= node[1]['eje_x']
        ejes_nodo[1]= node[1]['eje_y']

        d = distance_euclidean(ejes_nodo_objetivo,ejes_nodo)
        table[node[0]] = d
    return table


# Distancia Estimada al nodo objetivo
def h(idNodo,table):
    return table[idNodo]

# Distancia de arista entre el idNodo a la
def g(idNodo,idNodoIr,G):
    return G.get_edge_data(idNodo, idNodoIr)['peso']


def A_asterisk(G,sign_node_origen , sign_node_goal):

    try:
        id_node_origen = sign_node_origen
        id_node_goal = sign_node_goal

        L = [[G.nodes[id_node_origen]['sign']]]
        node_goal = G.nodes[id_node_goal]['sign']

        table = table_distance(G,node_goal)

    except ValueError:
        print("El nodo de origen origen o de destino escrito no existe")
        L = []
    except IndexError:
        print("El nodo de origen origen o de destino escrito no existe")
        L = []
    except KeyError:
        print("El nodo de origen origen o de destino escrito no existe")
        L = []

    # Nuestra L temporal para almcenar nuevos caminos que son posibles recorrer
    L_temp = []

    while (len(L) != 0):

        # n es el simbolo del nodo que nos encontramos
        n = L[0][0]

        if n == node_goal:
            # Retornamos todo el camino , lo invertimos porque el camino inicia con el nodo objetivo
            L[0].reverse()
            return L[0]
        else:
            signo_nodo_eliminado = n
            # print("Signo a Eliminar: ",signo_nodo_eliminado)

            id_nodo_eliminado = signo_nodo_eliminado
            # print("ID del Nodo a Eliminar: ",id_nodo_eliminado)

            # Guardamos el Camino recorrido
            path = L[0]
            L.pop(0)

            # Obtenemos la lista de los vecinos de los nodos
            list_id_vecinos = list(nx.neighbors(G, id_nodo_eliminado))
            # print("Lista de ID : ",list_id_vecinos)
            # print("Camino : ",path)

            # Obtener diccionarios con los pesos para llegar a ella
            diccionario_pesos_arista = {}
            for id_vecino in list_id_vecinos:
                peso = G.get_edge_data(id_nodo_eliminado,id_vecino)['peso']
                diccionario_pesos_arista[id_vecino] = peso

            # Sera un diccionario al inicio luego una lista
            peso_total_nodos = {}

            for id_vecino in list_id_vecinos:
                # print(index,id_vecino)
                # Guardamos en el diccionario primero el indice del nodo y luego el peso total
                # diccionario_peso_total[index] = [ id_vecino ,table[id_vecino] + diccionario_pesos_arista[id_vecino]]
                peso_total_nodos[id_vecino] =  table[id_vecino] + diccionario_pesos_arista[id_vecino]


            # Ordenar los id de los nodos por el peso total transformandolo en tuplas dentro de unalista
            peso_total_nodos = sorted(peso_total_nodos.items(), key = operator.itemgetter(1))
            # print(peso_total_nodos)
            # peso_total_nodos = [(ID_Nodo1, peso_total1),(ID_Nodo2, peso_total2)..]

            for tupla_id_peso in peso_total_nodos:
                simbolo_nuevo = tupla_id_peso[0]
                path_nuevo = path.copy()

                # Evitar bucles en el grafo es preguntar por el camino recorrido si hay un antecente
                # Si agrega el elemento entonces seguir por ese nodo
                if not simbolo_nuevo in path_nuevo:
                    path_nuevo.insert(0, simbolo_nuevo)
                    L_temp.append(path_nuevo)
                    break

            # for id_nbr in list_id_vecinos:
            #     simbolo_nuevo = G.nodes[id_nbr]['sign']
            #     path_nuevo = path.copy()
            #
            #     # Evitar bucles en el grafo es preguntar por el camino recorrido si hay un antecente
            #     if not simbolo_nuevo in path_nuevo:
            #         path_nuevo.insert(0, simbolo_nuevo)
            #         L_temp.append(path_nuevo)



            # Actualizamos la lista de L con la lista de nuevos caminos
            L = L_temp
            # print(L)

    else:
        print("No hay solucion")
        return None


def all_algoritm(G):
    opcion = int(input("Ingrese 1 si quieres eliminar nodos y 0 sino quiere eliminar ninguno: "))

    if opcion == 1:
        opcion = True
    else:
        opcion = False

    id_nodo_elimnar = 0
    while opcion:
        id_nodo_elimnar = int(input("Ingrese el nodo a eliminar: "))
        remove_nodo(G,id_nodo_elimnar)

        opcion=int(input("Ingrese 1 si quieres eliminar nodos y 0 sino quiere eliminar ninguno: "))
        if opcion == 1:
            opcion = True
        else:
            opcion = False


    sign_node_origen = int(input("Ingrese nodo origen: "))
    sign_node_goal = int(input("Ingrese nodo objetivo: "))

    path_dfs=[]
    path_bfs = []
    path_a_asterisco = []

    print("Opcion 1 solo DFS")
    print("Opcion 2 solo BFS")
    print("Opcion 3 solo A*")
    print("Opcion 4 solo DFS y BFS")
    print("Opcion 5 solo DFS ,BFS y A*")

    opcion = int(input("Ingrese la opcion: "))

    if opcion == 1:
        path_dfs = Dfs(G,sign_node_origen , sign_node_goal)
        print(path_dfs)
    elif opcion == 2:
        path_bfs = Bfs(G, sign_node_origen, sign_node_goal)
        print(path_bfs)
    elif opcion == 3:
        path_dfs = Dfs(G, sign_node_origen, sign_node_goal)
        path_bfs = Bfs(G, sign_node_origen, sign_node_goal)
        print(path_dfs)
        print(path_bfs)
    elif opcion == 4:
        path_a_asterisco=A_asterisk(G, sign_node_origen, sign_node_goal)
        print(path_a_asterisco)
    elif opcion == 5:
        path_dfs = Dfs(G, sign_node_origen, sign_node_goal)
        path_bfs = Bfs(G, sign_node_origen, sign_node_goal)
        path_a_asterisco = A_asterisk(G, sign_node_origen, sign_node_goal)

        print("Camino de DFS: ",path_dfs)
        print("Camino de BFS: ", path_bfs)
        print("Camino de A*: ", path_a_asterisco)

        plt.figure("DFS")
        draw_color_graph_mat(G,path_dfs)

        plt.figure("BFS")
        draw_color_graph_mat(G,path_bfs)

        plt.figure("A*")
        draw_color_graph_mat(G,path_a_asterisco)
        plt.show()

from display import Display
from search import Search

# Inicializamos display (n,n,tamaño de los bloques)
d = Display(100,100,20)
# Construimos las grilla 
grid, inicio, objetivo = d.make_grid(weight=True)

# print(grid,end="\n")

s = Search(grid,inicio, objetivo)
# Inicializamos la busqueda (grilla,punto_incial,punto_a_buscar)

d.reset_grid()

visited = s.BFS()
path = s.make_path()
d.draw_visited(visited)
d.draw_path(path)




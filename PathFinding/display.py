import pygame as pg
import random

class Display:
    def __init__(self, cols, rows, sizesq):
        self.columns, self.rows = cols, rows
        self.sizesq = sizesq
        self.width, self.height = size = cols*sizesq+1, rows*sizesq+1

        self.grid = {}
        self.inicio, self.objetivo = (0, 0), (cols - 1, rows - 1)

        pg.init()
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption('BFS')
        self.clock = pg.time.Clock()

        # colors
        self.c_bg = (0,0,0)
        self.c_fg = (200,200,200)
        self.c_walls = (100, 100, 100)
        self.c_inicio = (0, 200, 0)
        self.c_objetivo = (200, 0, 0)
        self.cg_inicio = (200, 50, 0)
        self.cg_end = (0, 50, 200)
        self.c_path = (20, 20, 20)

        self.running = True
        print("___________end_Inicialize_______________")

    def make_grid(self,weight=False):
        self.create_empty_grid()
        self.create_walls(weight=weight)
        return self.grid, self.inicio, self.objetivo

    def reset_grid(self, weight=False):
#         Color y dibujar la grilla
        self.screen.fill(self.c_bg)
        self.draw_grid(walls=True, weight=weight)

    def draw_grid(self, walls=False, weight=False):
#         Inicializamos
        sizesq = self.sizesq
        sx, sy = self.inicio
        tx, ty = self.objetivo
        font = pg.font.SysFont(None, 12)
#         Dibujamos los cuadrados
        for col in range(self.columns):
            for row in range(self.rows):
                if walls and (col, row) not in self.grid:
                    pg.draw.rect(self.screen, self.c_walls, (col * sizesq, row * sizesq, sizesq, sizesq))
                if weight and (col, row) in self.grid:
                    text = font.render(str(self.grid[(col, row)][2]), True, self.c_fg)
                    text_rect = text.get_rect()
                    text_rect.center = (col * sizesq + sizesq // 2, row * sizesq + sizesq // 2)
                    self.screen.blit(text, text_rect)
# Dibujamos punto inicial y final
        pg.draw.circle(self.screen, self.c_inicio, (sx*sizesq + sizesq//2, sy*sizesq + sizesq//2), int(sizesq*0.3))
        pg.draw.circle(self.screen, self.c_objetivo, (tx * sizesq + sizesq // 2, ty * sizesq + sizesq // 2), int(sizesq * 0.3))
# Dibujamos las lineas de los cuadrados
        for col in range(self.columns + 1):
            pg.draw.line(self.screen, self.c_fg, (col*sizesq, 0), (col*sizesq, self.width), 1)
        for row in range(self.rows + 1):
            pg.draw.line(self.screen, self.c_fg, (0, row * sizesq), (self.height, row * sizesq), 1)

    def create_empty_grid(self):
        for x in range(self.columns):
            for y in range(self.rows):
                self.grid[(x,y)] = (0,None,0)

    def create_walls(self, weight=False):
        sizesq = self.sizesq
        inicio = loop = True
        while loop:
            self.screen.fill(self.c_bg)
            mpos = pg.mouse.get_pos()
            pos = mpos[0] // sizesq, mpos[1] // sizesq

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    loop = False

                if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_MIDDLE:
                    if pos in self.grid:
                        if inicio:
                            self.inicio = pos
                        else:
                            self.objetivo = pos
                        inicio = not inicio

            if pg.mouse.get_pressed()[0]:
                if pos in self.grid and pos not in (self.inicio, self.objetivo):
                    del self.grid[pos]
            if pg.mouse.get_pressed()[2]:
                if pos not in self.grid:
                    self.grid[pos] = (0, None, random.randrange(1,6))

            self.draw_grid(walls=True, weight=weight)

            pg.display.update()

    def draw_visited(self, visited):
        sizesq = self.sizesq
        max_d = max([d for d ,_ ,_ in self.grid.values()])
        i = 0
        font = pg.font.SysFont(None, 14, bold=True)
        while self.quit_loop():
            x, y = visited[i]
            d, _, _ = self.grid[(x, y)]
#             color = self.get_color(d, max_d)
            color = (0,120,0)
            pg.draw.rect(self.screen, color, (x * sizesq, y * sizesq, sizesq, sizesq))
            self.draw_grid()

            i = min(i + 1, len(visited) - 1)
            pg.display.update()
            self.clock.tick(30)

    def draw_path(self, path):
        sizesq = self.sizesq
        i = 0
        while self.quit_loop():
            x, y = path[i]
            pg.draw.circle(self.screen, self.c_path, (x*sizesq + sizesq//2, y*sizesq+sizesq//2), int(sizesq*0.15))

            i = min(i+1, len(path)-1)
            pg.display.update()
            self.clock.tick(10)

    def quit_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return False
        return True


from py_expression_eval import Parser
from statistics import mean
import math
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
A = 10


def rastrigin(array_X):
    global A
    return A + sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in array_X])


def Rastrigin(*X, **kwargs):
    B = kwargs.get('b', 10)
    return B + sum([(x ** 2 - B * np.cos(2 * math.pi * x)) for x in X])


class Func_math:
    # [[[values_x_0][values_y_0][values_z_0]], [[values_x_1][values_y_1][values_z_1]]],
    generations = []
    sumas = []
    medias = []
    maximos = []

    len_population = 0
    len_generation = 0

    last_best_population = 0
    minors_element = 10000

    is_Rastrigin = False

    def __init__(self, exp, len_population, len_generation, is_Rastrigin=False):
        self.len_population = len_population
        self.len_generation = len_generation
        if is_Rastrigin:
            self.is_Rastrigin = is_Rastrigin
            # x_start_domain = -100
            # x_end_domain = 100

            # Se nota el dibujo de reastering
            x_start_domain = -10
            x_end_domain = 10

            # x_start_domain = 0
            # x_end_domain = 100

            self.x_domain = [x_start_domain, x_end_domain]

        else:
            self.exp = exp
            # x_start_domain = int(input("Dominio Inical de x: "))
            # x_end_domain = int(input("Dominio Final de x: "))

            x_start_domain = 4
            x_end_domain = 100

            self.x_domain = [x_start_domain, x_end_domain]

            # y_start_domain = int(input("Dominio Inical de y: "))
            # y_end_domain = int(input("Dominio Final de y: "))
            y_start_domain = 4
            y_end_domain = 100
            self.y_domain = [y_start_domain, y_end_domain]

            # z_start_domain = int(input("Dominio Inical de y: "))
            # z_end_domain = int(input("Dominio Final de y: "))
            z_start_domain = 4
            z_end_domain = 100
            self.z_domain = [z_start_domain, z_end_domain]

    def result_expr(self, values):
        p = Parser()
        return p.parse(self.exp).evaluate({'x': values[0], 'y': values[1], 'z': values[2]})

    def results_expr(self, array_x, array_y, array_z):
        array_results = []
        array_all_results = []

        # ----------------------
        # Parche
        while len(array_y) < self.len_population:
            array_y.append(self.last_best_population)

        while len(array_z) < self.len_population:
            array_z.append(self.last_best_population)
        # ----------------------

        values = []
        for i in range(len(array_x)):
            values.clear()
            values.append(array_x[i])
            values.append(array_y[i])
            values.append(array_z[i])
            array_results.append(self.result_expr(values))

            array_all_results.append([values.copy()])
            array_all_results[i].append(self.result_expr(values))

        self.sumas.append(sum(array_results))
        self.medias.append(mean(array_results))
        self.maximos.append(max(array_results))
        return array_all_results

    # -------------------------------------------------
    def results_expr_Rastrigin(self, array_x):
        array_results = []

        # ----------------------
        # Parche
        for array in array_x:
            while len(array) < self.len_population:
                array.append(self.last_best_population)
            # print(array)
            # print(len(array))

        # ----------------------

        # Es como si fuera mi fila de la tabla
        array_all_results = []
        for i, values_x in enumerate(array_x):
            ans = rastrigin(values_x)

            array_results.append(ans)

            array_all_results.append([values_x.copy()])
            array_all_results[i].append(ans)

            minor = min(values_x)
            if minor < self.minors_element:
                self.minors_element = minor

        self.sumas.append(sum(array_results))
        self.medias.append(mean(array_results))
        self.maximos.append(max(array_results))
        return array_all_results

    # -------------------------------------------------

    def add_generate(self, array_x, array_y, array_z):
        i = len(self.generations)
        new_generation = [array_x, array_y, array_z]
        self.generations.insert(i, new_generation)
        # print(self.generations)

    # -------------------------------------------------
    def add_generate_Rastrigin(self, array_array_x):
        i = len(self.generations)
        self.generations.insert(i, array_array_x)
        # print(self.generations)

    # -------------------------------------------------

    def print_generations(self):
        for i, generation in enumerate(self.generations):
            print("G", i, "°")
            # print("valores de x : ", generation[0])
            # print("valores de y : ", generation[1])
            # print("valores de z : ", generation[2])
            print("Maximo: ", self.maximos[i])
            print("Media: ", self.medias[i])
            # print("Suma: ", self.sumas[i])

    def draw_rasterign(self):

        X = np.linspace(self.minors_element, self.last_best_population, 100)
        Y = np.linspace(self.minors_element, self.last_best_population, 100)

        X, Y = np.meshgrid(X, Y)

        Z = Rastrigin(X, Y, B=10)

        fig = plt.figure()
        # Matplotlib 3.4. <
        # ax = fig.gca(projection='3d')
        # Matplotlib 3.4. >
        ax = plt.subplot(111, projection="3d")
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.plasma, linewidth=0, antialiased=False)


    def draw_generations(self):
        plt.figure(1)
        plt.xlabel("Generaciones")
        plt.ylabel("fitness value")

        plt.plot(self.maximos, 'o-', color='g')
        plt.plot(self.medias, 'o:')

        # Draw Rastering
        if self.is_Rastrigin:
            self.draw_rasterign()

        plt.show()

    # Formula de aptitud
    def func_aptitud(self, value):
        index_generation = len(self.generations) - 1
        return round(value / self.sumas[index_generation], 2)

    def value_hope(self, value):
        index_generation = len(self.generations) - 1
        return round(value / self.medias[index_generation], 2)

    def value_current(self, value):
        return round(value, 0)

    def getDomain_x(self):
        return self.x_domain

    def getDomain_y(self):
        return self.y_domain

    def getDomain_z(self):
        return self.z_domain

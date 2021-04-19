from py_expression_eval import Parser
from statistics import mean
from pylab import *
from mpl_toolkits.mplot3d import axes3d


class Func_math:
    # [[[values_x_0][values_y_0][values_z_0]], [[values_x_1][values_y_1][values_z_1]]],
    generations = []
    sumas = []
    medias = []
    maximos = []
    len_population = 0
    len_generation = 0

    def __init__(self, exp,len_population,len_generation):
        self.len_population = len_population
        self.len_generation = len_generation

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
        self.y_domain  = [y_start_domain, y_end_domain]

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

    def add_generate(self, array_x, array_y, array_z):
        i = len(self.generations)
        new_generation = [array_x, array_y, array_z]
        self.generations.insert(i, new_generation)


    def print_generations(self):
        for i, generation in enumerate(self.generations):

            print("G", i, "°")

            # print("valores de x : ", generation[0])
            # print("valores de y : ", generation[1])
            # print("valores de z : ", generation[2])

            print("Maximo: ", self.maximos[i])
            print("Media: ", self.medias[i])
            # print("Suma: ", self.sumas[i])

    def draw_generations(self):
        plt.figure(1)

        plt.xlabel("Generaciones")
        plt.ylabel("Maximos")

        plt.plot(self.maximos, 'o:')

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



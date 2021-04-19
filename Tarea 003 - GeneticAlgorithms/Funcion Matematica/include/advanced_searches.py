from include.funcion_matemtica import *
from include.selection import *
from include.cruzamiento import *

import random

func_math = None

population_x_values = None
population_y_values = None
population_z_values = None

population_x_binary = None
population_y_binary = None
population_z_binary = None

values_func_math = None


def create_func_math(len_population, len_generation):
    # print("Simbolos aceptados para la expresion acepatos = + - * / ** () ^ sin cos PI...")
    # Mas simbolos aceptados ver en -> https://pypi.org/project/py-expression-eval/

    # expr = input("Introduce la funcion en  terminos de x  y z: ")
    # Ejemplos de Funciones
    # expr = "(x**2)+(y**2)+(z**2)"
    # expr="x**2+3*y*z"
    # expr = "1 + x * cos(PI * x) + 4"
    # expr = "y*(x+z)"
    # expr = "(x**2)+(y**2)"
    # expr = "x/()"
    # expr = "cos(x)*sin(y)"
    expr = "(x^2/4)+ (y^2)/9 - z"
    print("Funcion a evaluar es:", expr)
    global func_math

    func_math = Func_math(expr, len_population, len_generation)


def generate_population_initial():
    global population_x_values
    global population_y_values
    global population_z_values
    global population_x_binary
    global population_y_binary
    global population_z_binary
    global func_math

    len_population = func_math.len_population

    # Generar numeros random con los dominios puestos
    population_x_values = random.sample(range(func_math.x_domain[0], func_math.x_domain[1]), len_population)
    population_y_values = random.sample(range(func_math.y_domain[0], func_math.y_domain[1]), len_population)
    population_z_values = random.sample(range(func_math.z_domain[0], func_math.z_domain[1]), len_population)

    # population_x_binary = to_binary_list(population_x_values)
    # population_y_binary = to_binary_list(population_y_values)
    # population_z_binary = to_binary_list(population_z_values)

    # Añadir generacion solo valores no ponemos binarios
    func_math.add_generate(population_x_values.copy(), population_y_values.copy(), population_z_values.copy())


def algortihm_genetic():
    global population_x_values
    global population_y_values
    global population_z_values

    global population_x_binary
    global population_y_binary
    global population_z_binary
    global func_math

    population_x_binary = []
    population_y_binary = []
    population_z_binary = []

    # len_population = int(input("Ingrese el numero de la Poblacion:"))
    # len_generation = int(input("Ingrese el numero de las generaciones:"))

    # Buenas parametros
    len_population = 20
    len_generation = 40

    create_func_math(len_population, len_generation)

    # Poblacion Inicial
    generate_population_initial()

    pseleci = []
    for i_generation in range(len_generation):
        # Aqui se obtiene obtiene la suma, medias y maximo
        math_func_values = func_math.results_expr(population_x_values, population_y_values, population_z_values)

        # print(math_func_values)

        # -----------------------Seleccion de la ruleta-----------------------
        math_func_values_update = seleccion_ruleta(func_math, math_func_values)
        # -----------------------Fin de la Seleccion de la ruleta-----------------------

        # -----------------------Algoritmo de cruzamiento-----------------------
        # La agrupacion es por parejas adyacentes
        population_in_binaries = cruzamiento(func_math.len_population, math_func_values_update)

        population_x_binary = population_in_binaries[0]
        population_y_binary = population_in_binaries[1]
        population_z_binary = population_in_binaries[2]
        # -----------------------Fin del Algoritmo de cruzamiento-----------------------

        # ----------------------Población----------------------
        # # Eliminar Poblacion Actual
        population_x_values.clear()
        population_y_values.clear()
        population_z_values.clear()

        #  Nueva poblacion ya cruzada en binarios debemos castearlos
        population_x_values = to_int_list(population_x_binary)
        population_y_values = to_int_list(population_y_binary)
        population_z_values = to_int_list(population_z_binary)

        # Añadimos la nueva poblacion aun no se agrega la suma, promedio y maximo
        func_math.add_generate(population_x_values.copy(), population_y_values.copy(), population_z_values.copy())
        # ----------------------Fin de Población----------------------

    # La llamamos para guardar suma, promedio y maximo de la ultima problacion agregada
    func_math.results_expr(population_x_values, population_y_values, population_z_values)

    func_math.print_generations()
    func_math.draw_generations()

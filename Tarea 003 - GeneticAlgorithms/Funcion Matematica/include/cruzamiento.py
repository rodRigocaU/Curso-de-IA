import random

def to_binary(number):
    return format(number, "b")

def to_int(binary):
    return int(binary, 2)

def to_binary_list(list_values):
    new_population_binary = []

    for value in list_values:
        value_binary = to_binary(value)
        new_population_binary.append(value_binary)

    return new_population_binary


def to_int_list(list_values_binaries):
    new_population_int = []

    for value_binary in list_values_binaries:
        value_int = to_int(value_binary)
        new_population_int.append(value_int)

    return new_population_int


def standar_binary(number1, number2):
    binary1 = to_binary(number1)
    binary2 = to_binary(number2)

    len_b1 = len(binary1)
    len_b2 = len(binary2)

    # Caso cuando el cruzamineto de numero como 0 o 1 para hacer cortes minimo debe ser de tamaño 2
    if len_b1==1 or len_b2==1:
        binary2 = binary2.zfill(2)
        binary1 = binary1.zfill(2)
    elif len_b1 < len_b2:
        binary1 = binary1.zfill(len_b2)
    else:
        binary2 = binary2.zfill(len_b1)
    binaries = [binary1, binary2]
    return binaries



def cruzamiento(len_population,math_func_values_update):
    population_x_binary=[]
    population_y_binary=[]
    population_z_binary=[]
    population_in_binaries=[]
    for i in range(0, len_population, 2):
        # -------------------x------------------------
        binaries_x = standar_binary(math_func_values_update[i][0][0], math_func_values_update[i + 1][0][0])
        # print("Binarios de x: ", binaries_x)

        len_binary_x = len(binaries_x[0])
        cross_position_x = random.randint(1, len_binary_x - 1)
        # print("Punto de Cruz x = ", cross_position_x)

        sub_binary_x_1_begin = binaries_x[0][:cross_position_x]
        sub_binary_x_1_end = binaries_x[0][cross_position_x:]
        sub_binary_x_2_begin = binaries_x[1][:cross_position_x]
        sub_binary_x_2_end = binaries_x[1][cross_position_x:]
        # print(sub_binary_x_1_begin, sub_binary_x_1_end)
        # print(sub_binary_x_2_begin, sub_binary_x_2_end)

        # Cruzamiento
        population_x_binary.append(sub_binary_x_1_begin + sub_binary_x_2_end)
        population_x_binary.append(sub_binary_x_2_begin + sub_binary_x_1_end)
        # print(population_x_binary)

        # -------------------y------------------------
        binaries_y = standar_binary(math_func_values_update[i][0][1], math_func_values_update[i + 1][0][1])
        # print("Binarios de y: ", binaries_y)
        len_binary_y = len(binaries_y[0])
        cross_position_y = random.randint(1, len_binary_y - 1)

        sub_binary_y_1_begin = binaries_y[0][:cross_position_y]
        sub_binary_y_1_end = binaries_y[0][cross_position_y:]
        sub_binary_y_2_begin = binaries_y[1][:cross_position_y]
        sub_binary_y_2_end = binaries_y[1][cross_position_y:]
        # print(sub_binary_y_1_begin, sub_binary_y_1_end)
        # print(sub_binary_y_2_begin, sub_binary_y_2_end)

        # Cruzamiento
        population_y_binary.append(sub_binary_y_1_begin + sub_binary_y_2_end)
        population_y_binary.append(sub_binary_y_2_begin + sub_binary_y_1_end)
        # print(population_y_binary)

        # -------------------z------------------------
        binaries_z = standar_binary(math_func_values_update[i][0][2], math_func_values_update[i + 1][0][2])
        # print("Binarios de z: ", binaries_z)
        len_binary_z = len(binaries_z[0])

        # ---------------------------------------------
        if len_binary_z == 1:
            print("Generacion :", i)
            print(binaries_z)
            print("Error por que el tamaño es 1")
        # ---------------------------------------------

        # Da error cuando ponemos randint(1,0) entonces len_binary_Z no debe salir 1
        cross_position_z = random.randint(1, len_binary_z - 1)

        sub_binary_z_1_begin = binaries_z[0][:cross_position_z]
        sub_binary_z_1_end = binaries_z[0][cross_position_z:]
        sub_binary_z_2_begin = binaries_z[1][:cross_position_z]
        sub_binary_z_2_end = binaries_z[1][cross_position_z:]
        # print(sub_binary_z_1_begin, sub_binary_z_1_end)
        # print(sub_binary_z_2_begin, sub_binary_z_2_end)

        # Cruzamiento
        population_z_binary.append(sub_binary_z_1_begin + sub_binary_z_2_end)
        population_z_binary.append(sub_binary_z_2_begin + sub_binary_z_1_end)
        # print(population_z_binary)
    population_in_binaries.append(population_x_binary)
    population_in_binaries.append(population_y_binary)
    population_in_binaries.append(population_z_binary)
    return population_in_binaries
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


def to_int_list_list(list_list_values_binaries):
    new_population_list_list_int = []
    for list_binarios in list_list_values_binaries:
        new_population_list_list_int.append(to_int_list(list_binarios))

    # for v in new_population_list_list_int:
    #     print(v)

    return new_population_list_list_int


def standar_binary(number1, number2):
    binary1 = to_binary(number1)
    binary2 = to_binary(number2)

    len_b1 = len(binary1)
    len_b2 = len(binary2)

    # Caso cuando el cruzamineto de numero como 0 o 1 para hacer cortes minimo debe ser de tamaño 2
    if len_b1 == 1 or len_b2 == 1:
        binary2 = binary2.zfill(3)
        binary1 = binary1.zfill(3)
    elif len_b1 < len_b2:
        binary1 = binary1.zfill(len_b2)
    else:
        binary2 = binary2.zfill(len_b1)
    binaries = [binary1, binary2]
    return binaries


def get_max_number(binary_number1, binary_number2):
    number1 = to_int(binary_number1)
    number2 = to_int(binary_number2)

    number_max = max(number1, number2)
    return to_binary(number_max)


def standar_binaries(array_number1, array_number2):
    binaries1 = to_binary_list(array_number1)
    binaries2 = to_binary_list(array_number2)

    # for i in range(0, len(binaries1), 2):
    for i in range(0, len(binaries1)):
        # Estandarizar los 0 a la izquierda
        len_b1 = len(binaries1[i])
        len_b2 = len(binaries2[i])

        # Caso cuando el cruzamineto de numero como 0 o 1 para hacer cortes minimo debe ser de tamaño 2
        if (len_b1 == 1) or (len_b2 == 1):
            binary1 = binaries1[i].zfill(2)
            binary2 = binaries2[i].zfill(2)
            binaries1[i] = binary1
            binaries2[i] = binary2


        elif len_b1 < len_b2:
            binary1 = binaries1[i].zfill(len_b2)
            binaries1[i] = binary1

        elif len_b2 < len_b1:
            binary2 = binaries2[i].zfill(len_b1)
            binaries2[i] = binary2
        else:
            continue

    binaries = [binaries1, binaries2]
    return binaries


def cruzamiento(len_population, math_func_values_update, func_math=None):

    population_x_binary = []

    all_item = []
    for v in math_func_values_update:
        all_item.extend(v[0])

    best_population = max(all_item)
    func_math.last_best_population = best_population
    best_population_binary = to_binary(best_population)

    if func_math.is_Rastrigin:
        domains = func_math.getDomain_x()
        population_in_binaries = []

        # Cada pareja
        for i in range(0, len_population, 2):

            binaries_couple_x = standar_binaries(math_func_values_update[i][0], math_func_values_update[i + 1][0])

            # Cruzar
            array_binaries_x_1 = []
            array_binaries_x_2 = []

            for j in range(len(binaries_couple_x[0])):
                # x0_0
                binary_x_copuple_1 = binaries_couple_x[0][j]
                # x1_0
                binary_x_copuple_2 = binaries_couple_x[1][j]

                # -------------------------------------------------------------------
                # Aplicar Elitismo (mantener el mejor de la generación anterior)
                if best_population_binary == binary_x_copuple_1 or best_population_binary == binary_x_copuple_1:
                    array_binaries_x_1.append(best_population_binary)
                    array_binaries_x_2.append(best_population_binary)
                # -------------------------------------------------------------------

                else:
                    len_binary_x = len(binary_x_copuple_1)
                    print(len_binary_x)
                    cross_position_x = random.randint(1, len_binary_x - 1)

                    sub_binary_x_1_begin = binary_x_copuple_1[:cross_position_x]
                    sub_binary_x_1_end = binary_x_copuple_1[cross_position_x:]
                    sub_binary_x_2_begin = binary_x_copuple_2[:cross_position_x]
                    sub_binary_x_2_end = binary_x_copuple_2[cross_position_x:]

                    # Cruzamiento
                    binary_first_cross = sub_binary_x_1_begin + sub_binary_x_2_end
                    binary_second_cross = sub_binary_x_2_begin + sub_binary_x_1_end

                    # Mantener el dominio de x
                    # -------------------------------------------------
                    max_number_binary = get_max_number(binary_x_copuple_1, binary_x_copuple_2)
                    number_1 = to_int(binary_first_cross)
                    number_2 = to_int(binary_second_cross)
                    # -------------------------------------------------
                    # sobrepasa el dominio
                    if (domains[0] > number_1 or number_1 > domains[1]) and \
                            (domains[0] > number_2 or number_2 > domains[1]):
                        # print("GA IF")
                        array_binaries_x_1.append(max_number_binary)
                        array_binaries_x_2.append(max_number_binary)
                        # array_binaries_x_1.append(binary_first_cross)
                        # array_binaries_x_2.append(binary_second_cross)

                    elif domains[0] > number_1 or number_1 > domains[1]:
                        # print("GA ELIF1")
                        array_binaries_x_1.append(max_number_binary)
                        # array_binaries_x_1.append(binary_first_cross)

                    elif domains[0] > number_2 or number_2 > domains[1]:
                        # print("GA ELIF2")
                        array_binaries_x_2.append(max_number_binary)
                        # array_binaries_x_2.append(binary_second_cross)

                    else:
                        # print("GA ELSE")
                        array_binaries_x_1.append(binary_first_cross)
                        array_binaries_x_2.append(binary_second_cross)

            population_in_binaries.append(array_binaries_x_1.copy())
            population_in_binaries.append(array_binaries_x_2.copy())

        return population_in_binaries

    else:
        domains_x = func_math.getDomain_x()
        domains_y = func_math.getDomain_y()
        domains_z = func_math.getDomain_z()

        population_y_binary = []
        population_z_binary = []
        population_in_binaries = []
        for i in range(0, len_population, 2):
            # -------------------x------------------------
            binaries_x = standar_binary(math_func_values_update[i][0][0], math_func_values_update[i + 1][0][0])

            len_binary_x = len(binaries_x[0])
            cross_position_x = random.randint(1, len_binary_x - 1)

            # Obtener la separación
            sub_binary_x_1_begin = binaries_x[0][:cross_position_x]
            sub_binary_x_1_end = binaries_x[0][cross_position_x:]
            sub_binary_x_2_begin = binaries_x[1][:cross_position_x]
            sub_binary_x_2_end = binaries_x[1][cross_position_x:]

            # Mantener el dominio
            child_1_binary = sub_binary_x_1_begin + sub_binary_x_2_end
            child_2_binary = sub_binary_x_2_begin + sub_binary_x_1_end

            child_1_number = to_int(child_1_binary)
            child_2_number = to_int(child_2_binary)
            max_number_binary = get_max_number(child_1_binary, child_2_binary)

            if (domains_x[0] > child_1_number or child_1_number > domains_x[1]) and \
                    (domains_x[0] > child_2_number or child_2_number > domains_x[1]):

                population_x_binary.append(max_number_binary)
                population_x_binary.append(max_number_binary)

            elif domains_x[0] > child_1_number or child_1_number > domains_x[1]:
                population_x_binary.append(max_number_binary)
                population_x_binary.append(child_2_binary)

            elif domains_x[0] > child_2_number or child_2_number > domains_x[1]:
                population_x_binary.append(child_1_binary)
                population_x_binary.append(max_number_binary)

            else:
                population_x_binary.append(child_1_binary)
                population_x_binary.append(child_2_binary)

            # -------------------y------------------------
            binaries_y = standar_binary(math_func_values_update[i][0][1], math_func_values_update[i + 1][0][1])
            len_binary_y = len(binaries_y[0])
            cross_position_y = random.randint(1, len_binary_y - 1)

            sub_binary_y_1_begin = binaries_y[0][:cross_position_y]
            sub_binary_y_1_end = binaries_y[0][cross_position_y:]
            sub_binary_y_2_begin = binaries_y[1][:cross_position_y]
            sub_binary_y_2_end = binaries_y[1][cross_position_y:]

            # --------------------------------------------------
            # Mantener el dominio
            child_1_binary = sub_binary_y_1_begin + sub_binary_y_2_end
            child_2_binary = sub_binary_y_2_begin + sub_binary_y_1_end

            child_1_number = to_int(child_1_binary)
            child_2_number = to_int(child_2_binary)
            max_number_binary = get_max_number(child_1_binary, child_2_binary)

            if (domains_y[0] > child_1_number or child_1_number > domains_y[1]) and \
                    (domains_y[0] > child_2_number or child_2_number > domains_y[1]):

                population_y_binary.append(max_number_binary)
                population_y_binary.append(max_number_binary)

            elif domains_y[0] > child_1_number or child_1_number > domains_y[1]:
                population_y_binary.append(max_number_binary)
                population_y_binary.append(child_2_binary)

            elif domains_y[0] > child_2_number or child_2_number > domains_y[1]:

                population_y_binary.append(child_1_binary)
                population_y_binary.append(max_number_binary)
            else:
                population_y_binary.append(child_1_binary)
                population_y_binary.append(child_2_binary)
            # --------------------------------------------------


            # -------------------z------------------------
            binaries_z = standar_binary(math_func_values_update[i][0][2], math_func_values_update[i + 1][0][2])
            # print("Binarios de z: ", binaries_z)
            len_binary_z = len(binaries_z[0])

            cross_position_z = random.randint(1, len_binary_z - 1)

            sub_binary_z_1_begin = binaries_z[0][:cross_position_z]
            sub_binary_z_1_end = binaries_z[0][cross_position_z:]
            sub_binary_z_2_begin = binaries_z[1][:cross_position_z]
            sub_binary_z_2_end = binaries_z[1][cross_position_z:]

            # --------------------------------------------------
            # Condicionales para que no sobresalga del dominio
            child_1_binary = sub_binary_z_1_begin + sub_binary_z_2_end
            child_2_binary = sub_binary_z_2_begin + sub_binary_z_1_end

            child_1_number = to_int(child_1_binary)
            child_2_number = to_int(child_2_binary)
            max_number_binary = get_max_number(child_1_binary, child_2_binary)

            # sobrepasa el dominio
            if (domains_z[0] > child_1_number or child_1_number > domains_z[1]) and \
                    (domains_z[0] > child_2_number or child_2_number > domains_z[1]):

                population_z_binary.append(max_number_binary)
                population_z_binary.append(max_number_binary)

            elif domains_z[0] > child_1_number or child_1_number > domains_z[1]:
                population_z_binary.append(max_number_binary)
                population_z_binary.append(child_2_binary)

            elif domains_z[0] > child_2_number or child_2_number > domains_z[1]:

                population_z_binary.append(child_1_binary)
                population_z_binary.append(max_number_binary)

            else:

                population_z_binary.append(child_1_binary)
                population_z_binary.append(child_2_binary)
            # --------------------------------------------------

        population_in_binaries.append(population_x_binary)
        population_in_binaries.append(population_y_binary)
        population_in_binaries.append(population_z_binary)
        return population_in_binaries

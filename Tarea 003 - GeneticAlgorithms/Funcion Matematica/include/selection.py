def valor_actual(elem):
    return elem[4]


def seleccion_ruleta(func_math, math_func_values):

    len_population = func_math.len_population

    if func_math.is_Rastrigin:
        for i, value in enumerate(math_func_values):

            pseleci = func_math.func_aptitud(value[1])
            math_func_values[i].append(pseleci)

            # Para el valor esperado se obtiene con el valor reeemplzados en la funcion
            value_hope = func_math.value_hope(value[1])
            math_func_values[i].append(value_hope)

            # El valor actual solo es un redondeo del valor esperado que lo obtubimos en la anterior linea
            value_current = func_math.value_current(value[3])
            math_func_values[i].append(value_current)

        # Ordenar el arreglo por el valor actual
        math_func_values.sort(key=valor_actual)
        math_func_values_update = []

        for i, value in enumerate(math_func_values):
            if value[4] >= 1:
                math_func_values_update.append(value)
                if value[4] > 1:
                    for j in range(1, int(value[4])):
                        math_func_values_update.append(value)

        # Completar la poblacion de elementos en caso que al repetirlos no alcanzara
        while len(math_func_values_update) < len_population:
            math_func_values_update.append(math_func_values[-1])

        while len(math_func_values_update) > len_population:
            math_func_values_update.pop()

        return math_func_values_update
    else:
        for i, value in enumerate(math_func_values):
            # Parametros son el valor y el indice de generacion
            pseleci = func_math.func_aptitud(value[1])
            math_func_values[i].append(pseleci)

            # Para el valor esperado se obtiene con el valor reeemplzados en la funcion
            value_hope = func_math.value_hope(value[1])
            math_func_values[i].append(value_hope)

            # El valor actual solo es un redondeo del valor esperado que lo obtubimos en la anterior linea
            value_current = func_math.value_current(value[3])
            math_func_values[i].append(value_current)

        # Ordenar el arreglo por el valor actual
        math_func_values.sort(key=valor_actual)

        math_func_values_update = []

        for i, value in enumerate(math_func_values):
            if value[4] >= 1:
                math_func_values_update.append(value)
                if value[4] > 1:
                    for j in range(1, int(value[4])):
                        math_func_values_update.append(value)

        # Completar la poblacion de elementos en caso que al repetirlos no alcanzara
        while len(math_func_values_update) < len_population:
            math_func_values_update.append(math_func_values[-1])

        return math_func_values_update

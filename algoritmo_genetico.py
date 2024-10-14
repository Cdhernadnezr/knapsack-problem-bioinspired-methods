import random
import matplotlib.pyplot as plt
import pandas as pd
import os
import time

capacidad_max = 2450

def leer_datos(archivo):
    datos = pd.read_excel(archivo, sheet_name='Hoja1')
    capacidad_maxima = capacidad_max
    items = []
    for i in range(len(datos)):
        valor = int(datos.iloc[i, 2])
        peso = int(1000 * datos.iloc[i, 1])
        cantidad = int(datos.iloc[i, 3])
        items.append((valor, peso, cantidad))
    return capacidad_maxima, items

def generar_poblacion(num_individuos, num_items, items, max_objetos):
    poblacion = []
    for _ in range(num_individuos):
        individuo = [random.randint(0, min(items[i][2], max_objetos)) for i in range(num_items)]  # Inicializar cantidad de cada objeto
        poblacion.append(individuo)
    return poblacion

def fitness(solucion, capacidad_maxima, items):
    peso = sum(solucion[i]* items[i][1] for i in range(len(solucion)))
    valor = sum(solucion[i]* items[i][0] for i in range(len(solucion)))
    if peso > capacidad_maxima:
        retorno = 0
    else:
        retorno = valor
    return retorno
    

def seleccionar_padres(poblacion):
    padres = random.sample(poblacion, 2)
    return padres

def crossover(padre1, padre2):
    punto_corte = random.randint(0, len(padre1) - 1)
    hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
    hijo2 = padre2[:punto_corte] + padre1[punto_corte:]
    return hijo1, hijo2

def mutar_individuo(individuo, prob_mutacion, max_objetos, items):
    cantidad_objetos = sum(individuo)
    if cantidad_objetos > max_objetos:  # Si la cantidad de objetos seleccionados excede el máximo, se reduce aleatoriamente
        exceso = cantidad_objetos - max_objetos
        for _ in range(exceso):
            idx = random.randint(0, len(individuo) - 1)
            if individuo[idx] > 0:
                individuo[idx] -= 1
    else:
        for i in range(len(individuo)):
            if random.random() < prob_mutacion:
                cantidad_maxima = items[i][2]
                individuo[i] = random.randint(0, min(cantidad_maxima, max_objetos))  # Cambiar la cantidad de objetos
    return individuo

def mutar_poblacion(poblacion, prob_mutacion, max_objetos, items):
    poblacion_mutada = []
    for individuo in poblacion:
        individuo_mutado = mutar_individuo(individuo, prob_mutacion, max_objetos, items)
        poblacion_mutada.append(individuo_mutado)
    return poblacion_mutada

def peso_total(solucion, items):
    peso = sum(solucion[i] * items[i][1] for i in range(len(solucion)))
    return peso

def algoritmo_genetico(archivo, tam_poblacion, num_generaciones, prob_cruce, prob_mutacion, tam_elite, tomar_todos, max_objetos):
    inicio = time.time()
    capacidad_maxima, items = leer_datos(archivo)
    mejores_fitness = []
    poblacion = generar_poblacion(tam_poblacion, len(items), items, max_objetos)

    mejor_valor = 0
    mejor_iteracion = 0
    mejor_peso = 0
    mejor_solucion = []

    poblacion_elite = []
    poblacion_elite_fitness = []  
    
    for generacion in range(num_generaciones):
        if tomar_todos:
            capacidad_max_generacion = capacidad_maxima
        else:
            capacidad_max_generacion = random.randint(capacidad_maxima // 2, capacidad_maxima)  

        evaluaciones = [(individuo, fitness(individuo, capacidad_max_generacion, items)) for individuo in poblacion]
        evaluaciones.sort(key=lambda x: x[1], reverse=True)
        poblacion = [individuo for individuo, _ in evaluaciones]
        mejor_fitness = evaluaciones[0][1]
        mejores_fitness.append(mejor_fitness)

        if mejor_fitness > mejor_valor:
            mejor_valor = mejor_fitness
            mejor_iteracion = generacion
            mejor_solucion = poblacion[0]
            mejor_peso = peso_total(mejor_solucion, items)

        # Actualizar la población elite
        if len(poblacion_elite) < tam_elite:
            poblacion_elite.append((mejor_solucion, mejor_fitness))
        else:
            peor_indice = min(range(len(poblacion_elite)), key=lambda x: poblacion_elite[x][1])
            if mejor_fitness > poblacion_elite[peor_indice][1]:
                poblacion_elite[peor_indice] = (mejor_solucion, mejor_fitness)

        poblacion_elite_fitness.append(max([fit for _, fit in poblacion_elite]))

        seleccionados = poblacion[:tam_poblacion // 2]

        hijos = []
        for i in range(0, len(seleccionados), 2):
            padre1, padre2 = seleccionar_padres(seleccionados)
            if random.random() < prob_cruce:
                hijo1, hijo2 = crossover(padre1, padre2)
                hijos.append(hijo1)
                hijos.append(hijo2)
            else:
                hijos.append(padre1)
                hijos.append(padre2)

        mutar_poblacion(hijos, prob_mutacion, max_objetos, items)

        poblacion = seleccionados + hijos
        
    fin = time.time()
    tiempo_empleado = fin - inicio
    
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, num_generaciones + 1), poblacion_elite_fitness, label='Mejor fitness')
    plt.xlabel('Generación')
    plt.ylabel('Fitness Máximo')
    plt.title('Convergencia del Algoritmo Genético')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print("Tiempo empleado: {0:.4f} seg". format(tiempo_empleado))
    temp = round(tiempo_empleado,4)
    print("Iteración la mejor solución:", mejor_iteracion)
    print("Peso de la mejor solución:", mejor_peso/1000)
    print("Valor óptimo:", mejor_valor)
    print("Mejor solución:", mejor_solucion)

    #Guarda los datos en un excel
    guardar_resultados_en_excel(1, mejor_valor, tiempo_empleado, mejor_iteracion, mejor_peso, mejor_solucion)

    return mejor_solucion, mejor_valor

def guardar_resultados_en_excel(nueva_corrida, valor_optimo, tiempo_empleado, mejor_iteracion, mejor_peso, mejor_solucion):
    #COLOCAR LA DIRECCIÓN DONDE SE QUIERA GUARDAR EL EXCEL CON LOS DATOS
    archivo_excel = 'resultadosGA1.xlsx'

    if os.path.isfile(archivo_excel):
        resultados = pd.read_excel(archivo_excel)
    else:
        resultados = pd.DataFrame(columns=['Corrida', 'Valor', 'Tiempo', 'Iteración', 'Peso', 'Mejor Solución'])

    nuevo_registro = pd.DataFrame({
        'Corrida': [nueva_corrida],
        'Valor': [valor_optimo],
        'Tiempo': [tiempo_empleado],
        'Iteración': [mejor_iteracion],
        'Peso': [mejor_peso],
        'Mejor Solución': [str(mejor_solucion)]
    })

    resultados = pd.concat([resultados, nuevo_registro], ignore_index=True)

    resultados.to_excel(archivo_excel, index=False)

#COLOCAR LA DIRECCIÓN EL ARCHIVO A ANALIZAR
archivo = 'Mochila_capacidad_maxima_2.45kg.xlsx'

tam_poblacion=100
num_generaciones=1000
prob_cruce = 0.8
prob_mutacion=0.1   
tam_elite = 5
max_objetos=15
solucion_optima, valor_optimo = algoritmo_genetico(archivo, tam_poblacion, num_generaciones, prob_cruce, prob_mutacion, tam_elite, False, max_objetos)

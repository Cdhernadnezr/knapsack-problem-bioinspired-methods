import numpy as np
import matplotlib.pyplot as plt
import time
import os
from collections import Counter
import pandas as pd

#COLOCAR LA DIRECCIÓN EL ARCHIVO A ANALIZAR
datos = pd.read_excel(r'Mochila_capacidad_maxima_2.45kg.xlsx', sheet_name='Hoja1')

items_tup=[(int(datos.iloc[i, 0]),int(1000*datos.iloc[i, 1]),int(datos.iloc[i, 2]),int(datos.iloc[i, 3])) for i in range(len(datos))]
start_time = time.time()
items= np.array(items_tup)

peso_maximo = 2450
num_hormigas = 20
num_iteraciones = 100
evaporacion = 0.1
feromona_inicial =0.9
alpha=1
beta =0.5

feromonas = np.ones(len(items)) * feromona_inicial
mejor_valor_global = 0
mejor_solucion_global = []
mejores_valores_por_iteracion = []

def seleccionar_item(peso_actual, seleccionados):
    pesos_disponibles = items[:,1] <= (peso_maximo - peso_actual)
    cantidades_disponibles = np.array([items[i, 3] - seleccionados.count(i) for i in range(len(items))]) > 0
    valor_heuristico = items[:,2] ** beta
    probabilidad = ((feromonas ** alpha) * valor_heuristico * pesos_disponibles * cantidades_disponibles)
    if probabilidad.sum() == 0:
        return None
    probabilidad /= probabilidad.sum()
    return np.random.choice(range(len(items)), p=probabilidad)

for iteracion in range(num_iteraciones):
    mejor_valor_iteracion = 0
    mejor_solucion_iteracion = []
    for hormiga in range(num_hormigas):
        solucion_actual = []
        seleccionados = []
        valor_actual = 0
        peso_actual = 0
        while True:
            item = seleccionar_item(peso_actual, seleccionados)
            if item is None or peso_actual + items[item,1] > peso_maximo:
                break
            solucion_actual.append(item)
            seleccionados.append(item)
            valor_actual += items[item,2]
            peso_actual += items[item,1]

        if valor_actual > mejor_valor_iteracion:
            mejor_valor_iteracion = valor_actual
            mejor_solucion_iteracion = solucion_actual
        
    if mejor_valor_iteracion > mejor_valor_global:
        mejor_valor_global = mejor_valor_iteracion
        mejor_solucion_global = mejor_solucion_iteracion
    
    mejores_valores_por_iteracion.append(mejor_valor_iteracion)
    
    for item in range(len(items)):
        feromonas[item] = (1-evaporacion) * feromonas[item] + sum([items[item,2] for s in mejor_solucion_iteracion if s == item]) / (mejor_valor_iteracion if mejor_valor_iteracion > 0 else 1)
    
finish_time = time.time()

duration = finish_time - start_time
indice_mejor_solucion = mejores_valores_por_iteracion.index(mejor_valor_global)

#Función para guardar excels
def guardar_resultados_en_excel(nueva_corrida, valor_optimo, tiempo_empleado, mejor_iteracion, mejor_peso, mejor_solucion):
    #COLOCAR LA DIRECCIÓN DONDE SE QUIERA GUARDAR EL EXCEL CON LOS DATOS
    archivo_excel = 'resultadosACO4.xlsx'

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

print ("Algoritmo de colonias de hormigas")
print(f"La mejor solución se alcanzó en la iteración número {indice_mejor_solucion + 1}.")
print(f"tiempo de duracion: {duration}")
print(f"Mejor Valor Global: {mejor_valor_global}")
print(f"Peso Total en gr: {sum(items[s,1] for s in mejor_solucion_global)}")

# Obtener la cuenta de cada ítem seleccionado
counter_solucion = Counter(mejor_solucion_global)

# Crear un arreglo que represente la cantidad seleccionada de cada ítem
solucion_completa = [counter_solucion.get(i, 0) for i in range(len(items))]


print(f"Mejor Solución Global (Cantidad de Ítems seleccionados): {solucion_completa}")

#Guarda los datos en un excel
guardar_resultados_en_excel(1, mejor_valor_global, duration, (indice_mejor_solucion+1), (sum(items[s,1] for s in mejor_solucion_global)), solucion_completa)


plt.plot(mejores_valores_por_iteracion, '-o', label='Mejor Valor por Iteración')
plt.title('Evolución del Mejor Valor por Iteración')
plt.xlabel('Iteración')
plt.ylabel('Fitness')
plt.legend()
plt.show()


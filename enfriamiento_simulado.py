import random
import math
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

class ProblemaMochila:
    def __init__(self, objetos, capacidad):
        self.objetos = objetos
        self.capacidad = capacidad

    def valor_total(self, solucion):
        """Calcula el valor total de los objetos seleccionados."""
        valor = 0
        for i in range(len(self.objetos)):
            if solucion[i] > 0:
                valor += self.objetos[i]["valor"] * solucion[i]
        return valor

    def peso_total(self, solucion):
        """Calcula el peso total de los objetos seleccionados."""
        peso = 0
        for i in range(len(self.objetos)):
            if solucion[i] > 0:
                peso += self.objetos[i]["peso"] * solucion[i]
        return peso

    def generar_solucion_inicial(self):
        """Genera una solución inicial válida."""
        solucion = [0] * len(self.objetos)
        peso_total = 0
        while peso_total <= self.capacidad:
            indice = random.randint(0, len(self.objetos) - 1)
            if peso_total + self.objetos[indice]["peso"] <= self.capacidad:
                solucion[indice] += 1
                peso_total += self.objetos[indice]["peso"]
            else:
                break
        return solucion

    def solucion_vecina(self, solucion_actual):
        """Genera una solución vecina."""
        vecino = solucion_actual.copy()
        for i in range(len(vecino)):
            if random.random() < 0.1:  # Probabilidad de cambiar el elemento
                vecino[i] = random.randint(0, min(self.objetos[i]["cantidad_disponible"], self.capacidad // self.objetos[i]["peso"]))
        return vecino

    def aceptacion(self, delta_valor, temperatura):
        """Calcula la probabilidad de aceptar una solución peor."""
        if delta_valor >= 0:
            return 1.0
        else:
            if temperatura == 0:
                return 0.0
            else:
                return math.exp(delta_valor / temperatura)

    def enfriamiento(self, temperatura_inicial, enfriamiento_factor, iteracion_actual, iteraciones_totales):
        """Reduce la temperatura de acuerdo a un esquema de enfriamiento."""
        nueva_temperatura = temperatura_inicial * (1.0 - iteracion_actual / iteraciones_totales) ** enfriamiento_factor
        if nueva_temperatura < 0.01:
            return 0.01
        else:
            return nueva_temperatura

    def resolver(self, temperatura_inicial, enfriamiento_factor, iteraciones_totales):
        """Resuelve el problema de la mochila utilizando enfriamiento simulado."""
        mejor_solucion = self.generar_solucion_inicial()
        mejor_valor = self.valor_total(mejor_solucion)
        mejor_peso = self.peso_total(mejor_solucion)
        mejor_iteracion = 0  # Inicializar la variable para almacenar la mejor iteración

        solucion_actual = mejor_solucion.copy()
        valor_actual = mejor_valor
        peso_actual = mejor_peso
        
        # Medir el tiempo inicial
        tiempo_inicial = time.time()

        # Almacenar valores óptimos encontrados en cada iteración para la gráfica de convergencia
        valores_optimos = []

        for i in range(iteraciones_totales):
            vecino = self.solucion_vecina(solucion_actual)
            valor_vecino = self.valor_total(vecino)
            peso_vecino = self.peso_total(vecino)

            if peso_vecino <= self.capacidad:
                delta_valor = valor_vecino - valor_actual
                if self.aceptacion(delta_valor, temperatura_inicial) > random.random():
                    solucion_actual = vecino.copy()
                    valor_actual = valor_vecino
                    peso_actual = peso_vecino

                    if valor_actual > mejor_valor:
                        mejor_solucion = solucion_actual.copy()
                        mejor_valor = valor_actual
                        mejor_peso = peso_actual
                        mejor_iteracion = i  # Actualizar la mejor iteración

            temperatura_inicial = self.enfriamiento(temperatura_inicial, enfriamiento_factor, i, iteraciones_totales)
            
            # Registrar el valor óptimo encontrado en cada iteración
            valores_optimos.append(mejor_valor)
            
        # Calcular el tiempo empleado
        tiempo_empleado = time.time() - tiempo_inicial

        # Imprimir la iteración en la que se alcanzó la mejor solución
        # print("La mejor solución se alcanzó en la iteración:", mejor_iteracion)

        return mejor_solucion, mejor_valor, mejor_peso, tiempo_empleado, valores_optimos, mejor_iteracion

# Ejemplo de uso
#COLOCAR LA DIRECCIÓN EL ARCHIVO A ANALIZAR
df = pd.read_excel('Mochila_capacidad_maxima_2.45kg.xlsx')

# Create a list of dictionaries
objetos = []
for index, row in df.iterrows():
    objetos.append({
        'id': row['Id'],
        'valor':  row['Valor'],
        'peso': int(1000*row['Peso_kg']),
        'cantidad_disponible': row['Cantidad']
    })

def guardar_resultados_en_excel(nueva_corrida, valor_optimo, tiempo_empleado, mejor_iteracion, mejor_peso, mejor_solucion):
    #COLOCAR LA DIRECCIÓN DONDE SE QUIERA GUARDAR EL EXCEL CON LOS DATOS
    archivo_excel = 'resultadosSA.xlsx'

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


capacidad = 2450  # Capacidad de la mochila

# Resolver el problema de la mochila
problema = ProblemaMochila(objetos, capacidad)
solucion_optima, valor_optimo, peso_optimo, tiempo_empleado, valores_optimos, mejor_iteracion = problema.resolver(100.0, 0.99, 500000)

# Imprimir resultados
print (f"La mejor solución la encuentra en la iteración: {mejor_iteracion}")
print("Tiempo empleado:", tiempo_empleado)
#print("Número de iteraciones:", len(valores_optimos))
print("Solución óptima:", solucion_optima)
print("Valor óptimo:", valor_optimo)
print("Peso de la mochila:", (peso_optimo/1000), "kg")

#Guarda los datos en un excel
guardar_resultados_en_excel(1, valor_optimo, tiempo_empleado, mejor_iteracion, peso_optimo, solucion_optima)

# Graficar la convergencia
plt.plot(valores_optimos)
plt.xlabel('Iteración')
plt.ylabel('Valor óptimo')
plt.title('Convergencia del algoritmo de enfriamiento simulado')
plt.grid(True)
plt.show()






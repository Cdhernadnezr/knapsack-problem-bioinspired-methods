# Knapsack Problem Solved with Bioinspired Algorithms

This project solves the 0-1 Knapsack Problem using three different bioinspired algorithms:
- Genetic Algorithm (`algoritmo_genetico.py`)
- Ant Colony Optimization (`colonias_de_hormigas.py`)
- Simulated Annealing (`enfriamiento_simulado.py`)

## Problem Description
The problem is to maximize the value of items packed in a knapsack without exceeding the weight limit. The maximum capacity of the knapsack in this case is 2.45kg (or 2450 grams). The input data for the problem is stored in the Excel file `Mochila_capacidad_maxima_2.45kg.xlsx`.

## Algorithms Implemented
1. **Genetic Algorithm (`algoritmo_genetico.py`)**:
   - Uses genetic evolution techniques such as selection, crossover, and mutation to solve the problem.
   - Results are stored in the `resultadosGA1.xlsx` file.

2. **Ant Colony Optimization (`colonias_de_hormigas.py`)**:
   - Simulates the behavior of ants to find the optimal solution.
   - Results are stored in the `resultadosACO4.xlsx` file.

3. **Simulated Annealing (`enfriamiento_simulado.py`)**:
   - Uses a probabilistic technique to explore the solution space by "cooling" the solution over time.
   - Results are stored in the `resultadosSA.xlsx` file.

## How to Run
Make sure to have the required libraries installed:
```bash
pip install numpy matplotlib pandas
```

**To run the scripts**, execute the following commands in your terminal:

```bash
python algoritmo_genetico.py
python colonias_de_hormigas.py
python enfriamiento_simulado.py
```
## Contributors
This project was developed with contributions from:

- [Cristopher Hernandez Romanos](https://github.com/Cdhernadnezr).
- [Deiner Cassiani Garcia]
- [Mauricio De La Hoz Figueroa]
- [Ruben Mejía Niebles ]

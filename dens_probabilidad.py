import integ_method as im
import mascara as mask
import pandas as pd
import numpy as np
import os

# Parámetros de la simulación
Lx, Ly = 1.0, 1.0  # Tamaño del dominio
Nx, Ny = 170, 100    # Número de puntos en cada dirección
num_estados = 2000    # Número de estados a calcular
formato = 'qc'
archivo_csv = f'output/eigenvalues_{formato}.csv'

# Crear la máscara y la matriz de diferencias finitas
mascara = mask.crear_mascara(Nx, Ny, formato=formato, frontera=True)

# Comprobar si el archivo ya existe para evitar recalcular
if not os.path.exists(archivo_csv):
    print("Calculando autovectores y guardando en CSV...")
    matriz = im.finite_difference(mascara)
    autovalores, autovectores = im.encontrar_autovalores(matriz, num_estados)
    
    # Guardar autovectores en CSV (transponemos para que las columnas sean los estados)
    df = pd.DataFrame(autovectores)
    df.to_csv(archivo_csv, index=False)
    print(f"Datos guardados en {archivo_csv}")
else:
    print(f"Leyendo autovectores desde {archivo_csv}...")
    df = pd.read_csv(archivo_csv)
    autovectores = df.values

# Graficar la densidad de probabilidad para el estado solicitado (altas energías)
im.plot_densidad_probabilidad(autovectores, mascara, 1730)


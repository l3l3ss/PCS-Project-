import integ_method as im
import mascara as mask
import pandas as pd
import numpy as np
import os

Lx, Ly = 1.0, 1.0
Nx, Ny = 170, 100
num_estados = 2000
formato = 'c'
archivo_csv = f'output/eigenvalues_{formato}.csv'

mascara = mask.crear_mascara(Nx, Ny, formato=formato, frontera=True)

if not os.path.exists(archivo_csv):
    print("Calculando autovectores...")
    matriz = im.finite_difference(mascara)
    autovalores, autovectores = im.encontrar_autovalores(matriz, num_estados)

    df = pd.DataFrame(autovectores)
    df.to_csv(archivo_csv, index=False)
    print(f"Datos guardados en {archivo_csv}")
else:
    print(f"Leyendo autovectores desde {archivo_csv}...")
    df = pd.read_csv(archivo_csv)
    autovectores = df.values

im.plot_densidad_probabilidad(autovectores, mascara, 1400)


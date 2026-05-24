import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse.linalg as spla
import integ_method as im
import mascara as mask
import os

# 1. Configurar
Nx, Ny = 170, 100
num_estados = 1000
mascara = mask.crear_mascara(Nx, Ny, formato='qc', frontera=True)

# 2. Calcular autovectores si no existe la matriz precalculada rápida
print("Calculando matriz MDF...")
L = im.finite_difference(mascara)
print(f"Calculando {num_estados} autovalores... esto puede tardar un momento.")
autovalores, autovectores = im.encontrar_autovalores(L, num_estados)

print("Cálculo terminado. Buscando cicatrices (Scars)...")
# 3. Buscar estados con alto IPR (Inverse Participation Ratio)
resultados = []
# Evaluamos los últimos 200 estados (mayor energía, comportamiento semiclásico)
for k in range(num_estados - 200, num_estados):
    psi = autovectores[:, k]
    prob = np.abs(psi)**2
    prob = prob / np.sum(prob)
    ipr = np.sum(prob**2)
    max_prob = np.max(prob)
    resultados.append((k, ipr, max_prob))

# Ordenar por IPR descendente
resultados.sort(key=lambda x: x[1], reverse=True)

# 4. Guardar las imágenes de los top 5 para analizarlos
if not os.path.exists('output'):
    os.makedirs('output')

print("Top 5 candidatos a Scars:")
for i, (k, ipr, max_p) in enumerate(resultados[:5]):
    print(f"Top {i+1}: k={k}, IPR={ipr:.6f}, MaxProb={max_p:.6f}")
    
    # Extraer y formatear la probabilidad en la malla
    psi = autovectores[:, k]
    prob = np.abs(psi)**2
    grid = np.zeros_like(mascara, dtype=float)
    grid[mascara] = prob
    
    # Guardar imagen solo del heatmap para que lo vea la IA/usuario rápido
    plt.figure(figsize=(8, 5))
    plt.imshow(grid, cmap='viridis', origin='lower')
    plt.title(f'Estado k={k}')
    plt.colorbar(label='|psi|^2')
    plt.savefig(f'output/auto_scar_k_{k}.png')
    plt.close()
    print(f"  Guardado output/auto_scar_k_{k}.png")

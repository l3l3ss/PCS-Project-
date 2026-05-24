import numpy as np
import scipy.sparse.linalg as spla
import integ_method as im
import mascara as mask
import os

Nx, Ny = 170, 100
num_estados = 850
print("Calculando mascara 'c'...")
mascara_c = mask.crear_mascara(Nx, Ny, formato='c', frontera=True)

print("Calculando matriz MDF...")
L = im.finite_difference(mascara_c)

print(f"Calculando {num_estados} autovalores...")
autovalores, autovectores = im.encontrar_autovalores(L, num_estados)

resultados = []
# Miramos alrededor del 800 (ej. 750 a 850)
for k in range(750, 850):
    psi = autovectores[:, k]
    prob = np.abs(psi)**2
    prob = prob / np.sum(prob)
    ipr = np.sum(prob**2)
    max_prob = np.max(prob)
    resultados.append((k, ipr, max_prob))

resultados.sort(key=lambda x: x[1], reverse=True)

print("Top 5 Scars en el estadio completo ('c') cerca de k=800:")
for i, (k, ipr, max_p) in enumerate(resultados[:5]):
    print(f"Top {i+1}: k={k}, IPR={ipr:.6f}, MaxProb={max_p:.6f}")
    
# Guardar imagenes y print ascii
from PIL import Image
def print_image_ascii(grid, width=80):
    # Normalize to 0-255
    g_min, g_max = grid.min(), grid.max()
    img_data = (255 * (grid - g_min) / (g_max - g_min)).astype(np.uint8)
    img = Image.fromarray(img_data)
    # Resize
    w, h = img.size
    height = int((h / w) * width * 0.5)
    img = img.resize((width, height))
    pixels = np.array(img)
    chars = " .:-=+*#%@"
    for row in pixels:
        # We need to flip y for printing because arrays print top-to-bottom
        pass
    for row in pixels[::-1]:
        line = "".join(chars[int(p / 256 * len(chars))] for p in row)
        print(line)

top_k = resultados[0][0]
psi = autovectores[:, top_k]
prob = np.abs(psi)**2
grid = np.zeros_like(mascara_c, dtype=float)
grid[mascara_c] = prob
print(f"\nASCII art para k={top_k}:")
print_image_ascii(grid)

top2_k = resultados[1][0]
psi2 = autovectores[:, top2_k]
prob2 = np.abs(psi2)**2
grid2 = np.zeros_like(mascara_c, dtype=float)
grid2[mascara_c] = prob2
print(f"\nASCII art para k={top2_k}:")
print_image_ascii(grid2)

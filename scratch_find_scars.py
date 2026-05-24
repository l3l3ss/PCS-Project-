import numpy as np
import csv

archivo_csv = 'output/eigenvalues_qc.csv'
print(f"Leyendo {archivo_csv} sin pandas...")

data = []
with open(archivo_csv, 'r') as f:
    # Saltar header si lo hay
    header = f.readline()
    for line in f:
        data.append([float(x) for x in line.strip().split(',')])

autovectores = np.array(data)
num_estados = autovectores.shape[1]
print(f"Total de estados: {num_estados}")

resultados = []
for k in range(num_estados - 200, num_estados):
    psi = autovectores[:, k]
    prob = np.abs(psi)**2
    prob = prob / np.sum(prob)
    
    ipr = np.sum(prob**2)
    max_prob = np.max(prob)
    
    resultados.append((k, ipr, max_prob))

resultados.sort(key=lambda x: x[1], reverse=True)

print("\nTop 10 estados más localizados (candidatos a scars) por IPR:")
for k, ipr, max_prob in resultados[:10]:
    print(f"k={k}, IPR={ipr:.6f}, MaxProb={max_prob:.6f}")

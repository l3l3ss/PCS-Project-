import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.sparse.linalg as spla

def finite_difference(mascara):
    ny = mascara.shape[0]
    nx = mascara.shape[1]
    print(f"Dimensiones malla: x={nx}, y={ny}")

    xi = yi = 0
    xf = yf = 1
    hx = (xf-xi)/(nx-1)
    hy = (yf-yi)/(ny-1)

    vecino_x = 1/hx**2
    vecino_y = 1/hy**2

    mapa_indices = np.full((ny, nx), -1, dtype=int)
    num_incog = 0

    for i in range(ny):
        for j in range(nx):
            if mascara[i, j]:
                mapa_indices[i, j] = num_incog
                num_incog += 1

    print(f"Número real de incógnitas (puntos True): {num_incog}")

    if num_incog == 0:
        raise ValueError("La máscara está vacía (todo False).")

    rows = []
    cols = []
    data = []

    for i in range(ny):
        for j in range(nx):
            if not mascara[i, j]:
                continue

            k_centro = mapa_indices[i, j]
            coef_diag = 0.0  

            if j > 0 and mascara[i, j-1]:
                k = mapa_indices[i, j-1]
                rows.append(k_centro)
                cols.append(k)
                data.append(vecino_x)
                coef_diag -= vecino_x

            if j < nx - 1 and mascara[i, j+1]:
                k = mapa_indices[i, j+1]
                rows.append(k_centro)
                cols.append(k)
                data.append(vecino_x)
                coef_diag -= vecino_x

            if i > 0 and mascara[i-1, j]:
                k = mapa_indices[i-1, j]
                rows.append(k_centro)
                cols.append(k)
                data.append(vecino_y)
                coef_diag -= vecino_y

            if i < ny - 1 and mascara[i+1, j]:
                k = mapa_indices[i+1, j]
                rows.append(k_centro)
                cols.append(k)
                data.append(vecino_y)
                coef_diag -= vecino_y

            rows.append(k_centro)
            cols.append(k_centro)
            data.append(coef_diag)

    L = sp.coo_matrix((data, (rows, cols)), shape=(num_incog, num_incog)).tocsr()
    print(f"Forma de la matriz L resultante: {L.shape}")

    es_simetrica = (L != L.T).nnz == 0
    print("Simetría:", es_simetrica)
    return L

def encontrar_autovalores(MDF, eig): 
    valores_propios, vectores_propios = spla.eigsh(MDF, k=eig, sigma=0.01)

    return valores_propios, vectores_propios

def espaciado(autovalores):
    return np.diff(autovalores)

def plot_densidad_probabilidad(autovectores, mascara, indice):
    psi = autovectores[:, indice]
    prob = np.abs(psi)**2
    total_prob = np.sum(prob)
    print(f"Probabilidad total (suma de |psi|^2): {total_prob:.4f}")
    grid = np.zeros_like(mascara, dtype=float)
    grid[mascara] = prob
    if indice < 0: 
        index = len(autovectores[0]) + indice
    else:
        index = indice

    X, Y = np.meshgrid(np.arange(mascara.shape[1]), np.arange(mascara.shape[0]))

    fig = plt.figure(figsize=(16, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122, projection='3d')

    im = ax1.imshow(grid, cmap='viridis', origin='lower')
    ax1.set_title(f'Densidad de probabilidad (mapa de color) - autovector {index}')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04, label=r'$|\psi(x,y)|^2$')

    surf = ax2.plot_surface(X, Y, grid, cmap='viridis', edgecolor='none')
    ax2.set_title(f'Densidad de probabilidad 3D - autovector {index}')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y', fontsize =10)
    ax2.set_zlabel(r'$|\psi(x,y)|^2$')
    ax2.view_init(elev=30, azim=-60)

    plt.tight_layout()
    plt.show()
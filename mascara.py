import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def crear_mascara(nx, ny, formato, frontera=True):
    if formato == 'r':
        mascara = np.ones((ny, nx), dtype=bool)
    elif formato == 'c':
        radio = ny / 2.0

        Y, X = np.ogrid[:ny, :nx]

        cy = (ny - 1) / 2.0

        cx1 = (ny - 1) / 2.0           
        cx2 = (nx - 1) - (ny - 1) / 2.0 

        dist_izq = (X - cx1)**2 + (Y - cy)**2
        dist_der = (X - cx2)**2 + (Y - cy)**2

        mascara_izq = dist_izq <= radio**2
        mascara_der = dist_der <= radio**2

        mascara_rect = (X >= cx1) & (X <= cx2)

        mascara = mascara_izq | mascara_der | mascara_rect
    elif formato == 'qc':
        radio = ny - 1.0
        if radio < 0: radio = 0

        Y, X = np.ogrid[:ny, :nx]

        cy = 0.0
        cx = (nx - 1) - radio

        dist = (X - cx)**2 + (Y - cy)**2

        mascara_circ = dist <= radio**2
        mascara_rect = X <= cx

        mascara = mascara_circ | mascara_rect
    else:
        raise ValueError("Formato inválido. Usa 'r', 'c' o 'qc'.")

    if frontera:
        mascara[0, :] = False
        mascara[-1, :] = False
        mascara[:, 0] = False
        mascara[:, -1] = False

    return mascara

def probar_mascaras(x=100, y=50):
    mascara_r = crear_mascara(x, y, 'r')
    mascara_c = crear_mascara(x, y, 'c')
    mascara_qc = crear_mascara(x, y, 'qc')

    cmap_personalizado = ListedColormap(['red', 'blue'])

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    axs[0].imshow(mascara_r, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    axs[0].set_title(f"Rectangular Mask ('r') - {x}x{y}")

    axs[1].imshow(mascara_c, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    axs[1].set_title(f"Stadium mask ('c') - {x}x{y}")

    axs[2].imshow(mascara_qc, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    axs[2].set_title(f"Stadium quarter mask ('qc') - {x}x{y}")

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    probar_mascaras(170, 100)

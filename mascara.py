import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def crear_mascara(nx, ny, formato, frontera=True):
    """
    Parámetros:
    nx (int): Anchura de la máscara (dimensión x, columnas).
    ny (int): Altura de la máscara (dimensión y, filas).
    """
    if formato == 'r':
        mascara = np.ones((ny, nx), dtype=bool)
    elif formato == 'c':
        # El radio ahora depende de la altura (ny)
        radio = ny / 2.0
        
        # Generar coordenadas: Y son las filas (ny), X las columnas (nx)
        Y, X = np.ogrid[:ny, :nx]
        
        # Centro en el eje vertical (filas, y)
        cy = (ny - 1) / 2.0
        
        # Centros en el eje horizontal (columnas, x)
        cx1 = (ny - 1) / 2.0           # Centro del semicírculo izquierdo
        cx2 = (nx - 1) - (ny - 1) / 2.0 # Centro del semicírculo derecho
        
        # Distancia a los centros
        dist_izq = (X - cx1)**2 + (Y - cy)**2
        dist_der = (X - cx2)**2 + (Y - cy)**2
        
        mascara_izq = dist_izq <= radio**2
        mascara_der = dist_der <= radio**2
        
        # El rectángulo central ahora se limita en el eje X
        mascara_rect = (X >= cx1) & (X <= cx2)
        
        mascara = mascara_izq | mascara_der | mascara_rect
    else:
        raise ValueError("Formato inválido. Usa 'r' o 'c'.")
    
    if frontera:
        mascara[0, :] = False
        mascara[-1, :] = False
        mascara[:, 0] = False
        mascara[:, -1] = False
    
    return mascara



def probar_mascaras(x=100, y=50):
    """
    Función de prueba para visualizar las máscaras creadas usando matplotlib.
    Los valores válidos (True) se muestran en azul y los inválidos (False) en rojo.
    """
    mascara_r = crear_mascara(x, y, 'r')
    mascara_c = crear_mascara(x, y, 'c')
    
    # Crear mapa de colores: 0/False = rojo, 1/True = azul
    cmap_personalizado = ListedColormap(['red', 'blue'])
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    
    # Mostrar máscara rectangular (transponemos para que x sea horizontal e y vertical)
    axs[0].imshow(mascara_r.T, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    axs[0].set_title(f"Máscara Rectangular ('r') - {x}x{y}")
    
    # Mostrar máscara estadio (transponemos para que x sea horizontal e y vertical)
    axs[1].imshow(mascara_c.T, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    axs[1].set_title(f"Máscara Estadio ('c') - {x}x{y}")
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    probar_mascaras()

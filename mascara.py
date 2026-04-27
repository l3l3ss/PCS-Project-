import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def crear_mascara(x, y, formato):
    """
    Crea un array 2D de dimensiones (y, x) que funciona como máscara.
    
    Parámetros:
    x (int): Ancho de la máscara (número de columnas).
    y (int): Alto de la máscara (número de filas).
    formato (str): 'r' para rectángulo, 'c' para circular/estadio.
    
    Retorna:
    np.ndarray: Array de booleanos que representa la máscara.
    """
    if formato == 'r':
        return np.ones((y, x), dtype=bool)
    elif formato == 'c':
        radio = y / 2.0
        
        # Generar una grilla de coordenadas
        Y, X = np.ogrid[:y, :x]
        
        # Para que quede centrado en los índices del array, usamos (dim - 1) / 2
        cy = (y - 1) / 2.0
        cx1 = (y - 1) / 2.0
        cx2 = (x - 1) - (y - 1) / 2.0
        
        # Si x es menor que y, ajustamos los centros para mantener una lógica segura
        if cx1 > cx2:
            cx1, cx2 = cx2, cx1
            
        # Distancia al cuadrado a los centros de los círculos de los extremos
        dist_izq = (X - cx1)**2 + (Y - cy)**2
        dist_der = (X - cx2)**2 + (Y - cy)**2
        
        # Máscaras de los círculos (evaluadas con el radio al cuadrado)
        mascara_izq = dist_izq <= radio**2
        mascara_der = dist_der <= radio**2
        
        # Máscara del rectángulo central que une los dos círculos
        mascara_rect = (X >= cx1) & (X <= cx2)
        
        # La máscara final es la unión de los dos círculos y el rectángulo central
        return mascara_izq | mascara_der | mascara_rect
    else:
        raise ValueError("Formato inválido. Usa 'r' (rectangular) o 'c' (circular/estadio).")



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
    
    # Mostrar máscara rectangular
    axs[0].imshow(mascara_r, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    axs[0].set_title(f"Máscara Rectangular ('r') - {x}x{y}")
    
    # Mostrar máscara estadio
    axs[1].imshow(mascara_c, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    axs[1].set_title(f"Máscara Estadio ('c') - {x}x{y}")
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    probar_mascaras()

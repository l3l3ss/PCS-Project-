import warnings
import numpy as np
from scipy.signal import convolve2d, find_peaks
from scipy.special import y0
import scipy.linalg as la

def extraer_frontera(mascara):
    """
    Dada una máscara booleana 2D, identifica los píxeles que forman la frontera.
    Esto es el primer paso para el Boundary Element Method (BEM).
    """
    kernel = np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]])
    
    vecinos_true = convolve2d(mascara.astype(int), kernel, mode='same', boundary='fill', fillvalue=0)
    frontera = mascara & (vecinos_true < 5)
    return frontera

def boundary_element_method(mascara):
    """
    BEM extrae y trabaja únicamente sobre la frontera 1D.
    Mapea las coordenadas a la escala física (caja de 1x1) usada en integ_method.py.
    """
    ny, nx = mascara.shape
    hx = 1.0 / (nx - 1)
    hy = 1.0 / (ny - 1)
    
    frontera = extraer_frontera(mascara)
    y_borde, x_borde = np.where(frontera)
    
    num_original = len(x_borde)
    
    # El perímetro aproximado es la cantidad de puntos por el paso de red promedio
    h_grid = (hx + hy) / 2.0
    perimetro_aprox = num_original * h_grid
    
    # Submuestreamos la frontera para que la matriz no sea gigantesca y el cálculo sea rápido
    max_puntos = 200
    if len(x_borde) > max_puntos:
        step = len(x_borde) // max_puntos
        x_borde = x_borde[::step]
        y_borde = y_borde[::step]
        
    num_puntos = len(x_borde)
    h_eff = perimetro_aprox / num_puntos  # Espaciado efectivo entre puntos
    
    x_phys = x_borde * hx
    y_phys = y_borde * hy
    
    puntos_frontera = np.column_stack((x_phys, y_phys))
    
    # Pre-calculamos la matriz de distancias
    diff = puntos_frontera[:, np.newaxis, :] - puntos_frontera[np.newaxis, :, :]
    dist_matrix = np.linalg.norm(diff, axis=-1)
    
    print(f"BEM: Dominio 2D reducido a {num_puntos} elementos de frontera (1D).")
    
    # Retornamos un diccionario con todo lo necesario para encontrar_autovalores
    return {
        'dist_matrix': dist_matrix,
        'h_eff': h_eff,
        'num_puntos': num_puntos
    }

def encontrar_autovalores(borde, eig, k_min=2.0, k_max=None, dk=0.025):
    """
    Encuentra los autovalores usando BEM resolviendo det(M(k)) = 0.
    Para ello, buscamos los mínimos locales del valor absoluto del autovalor
    más pequeño de la matriz simétrica M(k) construida con la función de Bessel Y_0.
    """
    dist_matrix = borde['dist_matrix']
    h_eff = borde['h_eff']
    num_puntos = borde['num_puntos']
    
    # Estimación de k_max mediante la Ley de Weyl para billares 2D:
    # N(k) ~ (Area / 4*pi) * k^2 => k ~ sqrt(4 * pi * N / Area)
    # Como todo está en una caja de 1x1, el Area es del orden de ~0.8
    if k_max is None:
        k_max_estimado = np.sqrt(4.0 * np.pi * eig / 0.8) * 1.05 # Añadimos 5% de margen
        k_max = k_max_estimado
        
    print(f"BEM: Buscando {eig} autovalores mediante barrido en k in [{k_min:.1f}, {k_max:.1f}] con paso {dk}...")
    
    k_vals = np.arange(k_min, k_max, dk)
    min_eigenval_abs = np.zeros_like(k_vals)
    
    # Usamos np.euler_gamma = 0.5772...
    gamma = np.euler_gamma
    
    # Pre-inicializar la matriz para no reservar memoria en cada ciclo
    M = np.zeros_like(dist_matrix)
    
    # Para ignorar el RuntimeWarning de y0(0) en la diagonal (que sobrescribimos de todos modos)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        for i, k in enumerate(k_vals):
            # Elementos fuera de la diagonal: y0(k * d_ij)
            M = y0(k * dist_matrix)
            
            # Elementos en la diagonal (integración de la singularidad sobre el elemento h_eff)
            diag_val = (2.0 / np.pi) * (np.log(k * h_eff / 4.0) + gamma - 1.0)
            np.fill_diagonal(M, diag_val)
            
            # Buscamos el autovalor de menor magnitud (el que se acerca a 0 cuando el determinante es 0)
            evals = la.eigvalsh(M)
            min_eigenval_abs[i] = np.min(np.abs(evals))
            
            if i > 0 and i % 1000 == 0:
                print(f"  -> Progreso: barrido hasta k={k:.2f} completado...")

    # Buscamos los valles (mínimos locales) invirtiendo el signo para usar find_peaks
    peaks, properties = find_peaks(-min_eigenval_abs)
    autovalores_k = k_vals[peaks]
    
    # Nos quedamos con los primeros 'eig'
    if len(autovalores_k) > eig:
        autovalores_k = autovalores_k[:eig]
        
    print(f"BEM completado: Se encontraron {len(autovalores_k)} autovalores.")
    
    if len(autovalores_k) < eig:
        print(f"  Aviso: Se encontraron menos autovalores de los solicitados ({eig}).")
        print("  Puedes intentar aumentar k_max o reducir dk para mayor precisión.")
        
    return autovalores_k

def espaciado(autovalores):
    """
    Calcula la diferencia (s_i = E_{i+1} - E_i) entre niveles de energía adyacentes.
    """
    return np.diff(autovalores)

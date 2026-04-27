import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import numpy as np
import scipy.sparse as sp

def finite_difference_simple(nx, ny):
    """
    Versión simplificada que usa el mismo esquema de indexación que finite_difference.
    nx, ny son las dimensiones de la malla física (incluyendo frontera).
    """
    xi = yi = 0
    xf = yf = 1 
    hx = (xf-xi)/(nx-1)
    hy = (yf-yi)/(ny-1)

    num_incog = (nx-2)*(ny-2)  # puntos internos
    coef_centro = -2/hx**2 - 2/hy**2 
    vecino_x = 1/hx**2
    vecino_y = 1/hy**2

    # El salto en dirección y es igual al número de puntos por fila interna
    salto_y = ny - 2  # número de columnas internas
    
    # En finite_difference:
    # - vecinos en j±1 usan vecino_y → salto de 1, pero NO entre filas
    # - vecinos en i±1 usan vecino_x → salto de ny-2
    # Por tanto, NO debemos conectar puntos entre filas con diagonal ±1
    
    diag_central = coef_centro * np.ones(num_incog)
    
    # Para las diagonales ±1 (vecino_y), NO debemos conectar entre filas
    # Cada fila tiene salto_y puntos, así que el último índice de cada fila es:
    # fila 0: 0 a salto_y-1 → último = salto_y-1
    # fila 1: salto_y a 2*salto_y-1 → último = 2*salto_y-1
    # Por tanto, no hay conexión entre (k) y (k+1) cuando k % salto_y == salto_y - 1
    
    # Crear vectores para las diagonales ±1 excluyendo los saltos de fila
    diag_1 = np.zeros(num_incog - 1)
    for k in range(num_incog - 1):
        # Si k es el último de su fila, no hay conexión al siguiente
        if (k + 1) % salto_y == 0:
            diag_1[k] = 0  # No hay vecino en esta posición
        else:
            diag_1[k] = vecino_y
    
    # La diagonal de salto_y usa vecino_x
    diag_ny = vecino_x * np.ones(num_incog - salto_y)

    L = sp.diags([diag_central, diag_1, diag_1, diag_ny, diag_ny], 
                 [0, 1, -1, salto_y, -salto_y], format="csr")
    print(L.shape)
    return L 

def finite_difference(mascara):
    nx = mascara.shape[0]
    ny = mascara.shape[1]
    print(f"Dimensiones de la malla física: nx={nx}, ny={ny}")
    
    xi = yi = 0
    xf = yf = 1
    hx = (xf-xi)/(nx-1)
    hy = (yf-yi)/(ny-1)

    coef_centro = -2/hx**2 - 2/hy**2 
    vecino_x = 1/hx**2
    vecino_y = 1/hy**2

    # --- PASO 1: CREAR EL MAPA DE ÍNDICES ---
    # Una matriz del mismo tamaño que la malla, llena de -1
    mapa_indices = np.full((nx, ny), -1, dtype=int)
    num_incog = 0
    
    # Asignamos un número de incógnita (0, 1, 2...) solo donde la máscara es True
    for i in range(nx):
        for j in range(ny):
            if mascara[i, j]:
                mapa_indices[i, j] = num_incog
                num_incog += 1
                
    print(f"Número real de incógnitas (puntos True): {num_incog}")
    
    if num_incog == 0:
        raise ValueError("La máscara está vacía (todo False).")

    # --- PASO 2: CONSTRUIR LA MATRIZ L ---
    # Usaremos listas para guardar la fila, la columna y el valor de cada elemento
    rows = []
    cols = []
    data = []

    for i in range(nx):
        for j in range(ny):
            if not mascara[i, j]:
                continue # Si es False, lo ignoramos por completo
                
            k_centro = mapa_indices[i, j] # El índice 1D de nuestro punto actual

            # 1. Añadimos la diagonal principal
            rows.append(k_centro)
            cols.append(k_centro)
            data.append(coef_centro)

            # 2. Comprobamos el vecino izquierdo (i-1)
            if i > 0 and mascara[i-1, j]:
                k_izq = mapa_indices[i-1, j]
                rows.append(k_centro)
                cols.append(k_izq)
                data.append(vecino_x)

            # 3. Comprobamos el vecino derecho (i+1)
            if i < nx - 1 and mascara[i+1, j]:
                k_der = mapa_indices[i+1, j]
                rows.append(k_centro)
                cols.append(k_der)
                data.append(vecino_x)

            # 4. Comprobamos el vecino de abajo (j-1)
            if j > 0 and mascara[i, j-1]:
                k_aba = mapa_indices[i, j-1]
                rows.append(k_centro)
                cols.append(k_aba)
                data.append(vecino_y)

            # 5. Comprobamos el vecino de arriba (j+1)
            if j < ny - 1 and mascara[i, j+1]:
                k_arr = mapa_indices[i, j+1]
                rows.append(k_centro)
                cols.append(k_arr)
                data.append(vecino_y)

    # Creamos la matriz dispersa a partir de las coordenadas
    L = sp.coo_matrix((data, (rows, cols)), shape=(num_incog, num_incog)).tocsr()
    print(f"Forma de la matriz L resultante: {L.shape}")
    
    return L

def encontrar_autovalores(MDF, eig): #MDF es la matrizz de difs finitas que se calcula en la funcion anterior, eig el número de autovalores que queremos encontrar
    valores_propios, vectores_propios = spla.eigsh(MDF, k=eig, which='SM')
    #los valores propios que se sacan arriba son en realidad k**2, los convertimos 

    eigenvalues = np.sqrt(-valores_propios)
    return eigenvalues



##Funcion creada con pablo para hacer prueba
def crear_mascara(x, y, formato, frontera=True):
    """
    Crea un array 2D de dimensiones (y, x) que funciona como máscara.
    
    Parámetros:
    x (int): Ancho de la máscara (número de columnas).
    y (int): Alto de la máscara (número de filas).
    formato (str): 'r' para rectángulo, 'c' para circular/estadio.
    frontera (bool): Si True, excluye los puntos de frontera (borde exterior).
    
    Retorna:
    np.ndarray: Array de booleanos que representa la máscara.
    """
    if formato == 'r':
        mascara = np.ones((y, x), dtype=bool)
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
        mascara = mascara_izq | mascara_der | mascara_rect
    else:
        raise ValueError("Formato inválido. Usa 'r' (rectangular) o 'c' (circular/estadio).")
    
    # Eliminar frontera (borde exterior)
    if frontera:
        mascara[0, :] = False
        mascara[-1, :] = False
        mascara[:, 0] = False
        mascara[:, -1] = False
    
    return mascara
    


mascara = crear_mascara(50, 100, 'r')
A_simple = finite_difference_simple(50, 100)
A_mascara = finite_difference(mascara)
autov_simple = np.sort(encontrar_autovalores(A_simple, 500))
autov_mascara = np.sort(encontrar_autovalores(A_mascara, 500))


diferencias_autovalores = autov_simple - autov_mascara
print(diferencias_autovalores)
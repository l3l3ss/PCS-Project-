import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def finite_difference(mascara):
    # En la matriz, la dimensión 0 son las filas (altura, y) 
    # y la dimensión 1 son las columnas (anchura, x)
    ny = mascara.shape[0] # Altura
    nx = mascara.shape[1] # Anchura
    print(f"Dimensiones de la malla física: anchura x={nx}, altura y={ny}")
    
    xi = yi = 0
    xf = yf = 1
    hx = (xf-xi)/(nx-1)
    hy = (yf-yi)/(ny-1)

    vecino_x = 1/hx**2
    vecino_y = 1/hy**2

    # --- PASO 1: CREAR EL MAPA DE ÍNDICES ---
    # Una matriz del mismo tamaño que la malla, llena de -1
    mapa_indices = np.full((ny, nx), -1, dtype=int)
    num_incog = 0
    
    # Recorremos por filas (i -> y) y luego columnas (j -> x)
    for i in range(ny):
        for j in range(nx):
            if mascara[i, j]:
                mapa_indices[i, j] = num_incog
                num_incog += 1
                
    print(f"Número real de incógnitas (puntos True): {num_incog}")
    
    if num_incog == 0:
        raise ValueError("La máscara está vacía (todo False).")

    # --- PASO 2: CONSTRUIR LA MATRIZ L ---
    rows = []
    cols = []
    data = []

    for i in range(ny):
        for j in range(nx):
            if not mascara[i, j]:
                continue
                    
            k_centro = mapa_indices[i, j]
            coef_diag = 0.0  

            # Vecino izquierda (eje x, cambiamos j-1)
            if j > 0 and mascara[i, j-1]:
                k = mapa_indices[i, j-1]
                rows.append(k_centro)
                cols.append(k)
                data.append(vecino_x)
                coef_diag -= vecino_x

            # Vecino derecha (eje x, cambiamos j+1)
            if j < nx - 1 and mascara[i, j+1]:
                k = mapa_indices[i, j+1]
                rows.append(k_centro)
                cols.append(k)
                data.append(vecino_x)
                coef_diag -= vecino_x

            # Vecino arriba (eje y, cambiamos i-1)
            if i > 0 and mascara[i-1, j]:
                k = mapa_indices[i-1, j]
                rows.append(k_centro)
                cols.append(k)
                data.append(vecino_y)
                coef_diag -= vecino_y

            # Vecino abajo (eje y, cambiamos i+1)
            if i < ny - 1 and mascara[i+1, j]:
                k = mapa_indices[i+1, j]
                rows.append(k_centro)
                cols.append(k)
                data.append(vecino_y)
                coef_diag -= vecino_y

            # Diagonal
            rows.append(k_centro)
            cols.append(k_centro)
            data.append(coef_diag)

    # Creamos la matriz dispersa
    L = sp.coo_matrix((data, (rows, cols)), shape=(num_incog, num_incog)).tocsr()
    print(f"Forma de la matriz L resultante: {L.shape}")
    print("Simetría:", np.allclose(L.toarray(), L.toarray().T))
    return L

def encontrar_autovalores(MDF, eig): 
    valores_propios, vectores_propios = spla.eigsh(MDF, k=eig, which='SM')
    
    # AÑADIDO: np.abs para evitar el RuntimeWarning (raíz de números negativos por precisión)
    eigenvalues = np.sqrt(np.abs(valores_propios))
    return eigenvalues

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

# === PRUEBA FINAL ===
# Ahora pasamos (anchura=100, altura=50)
mascara_estadio = crear_mascara(100, 50, 'c')
mascara_rectangulo = crear_mascara(100, 50, 'r')

A_estadio = finite_difference(mascara_estadio)
A_rectangulo = finite_difference(mascara_rectangulo)

autoval_estadio = np.sort(encontrar_autovalores(A_estadio, 40))
autoval_rectangulo = np.sort(encontrar_autovalores(A_rectangulo, 40))

# Ahora las dimensiones (num_incog) del estadio y rectángulo serán DIFERENTES.
# Por lo tanto, no se pueden restar directamente si no coinciden los tamaños, 
# pero puedes imprimir los primeros 10 de cada uno para comparar:
print("\nPrimeros 5 autovalores Estadio:")
print(autoval_estadio[:5])

print("\nPrimeros 5 autovalores Rectángulo:")
print(autoval_rectangulo[:5])

print(autoval_estadio-autoval_rectangulo)
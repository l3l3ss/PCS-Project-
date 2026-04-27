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

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def finite_difference(nx, ny):
    #nx, ny son el número de cuadrados en los que discretizamos el espacio
    xi = yi = 0
    xf = yf = 1 #distancia normalizada 
    hx = (xf-xi)/(nx-1)
    hy = (yf -yi)/(ny-1)

    num_incog = (nx-2)*(ny-2) #le resto los puntos de frontera tanto en x como en y 
    coef_centro = (-2/hx**2 - 2/hy**2) 
    vecino_x = 1/hx**2
    vecino_y = 1/hy**2

    diag_central = coef_centro** np.ones(num_incog) # la dimeneción de números en la diagnonal equivale al número más grande de x o y 
    diag_x = vecino_x*np.ones(num_incog-1)
    diag_y = vecino_y * np.ones(num_incog - nx)

    #La ecuación a resolver será Lp = \lambda p 
    L = sp.diags([diag_central, diag_x, diag_x, diag_y, diag_y], [0, 1, -1, nx, -nx], format="csr")
    print(L.shape)
    #print(L)
    return L 

def encontrar_autovalores(MDF, eig): #MDF es la matrizz de difs finitas que se calcula en la funcion anterior, eig el número de autovalores que queremos encontrar
    valores_propios, vectores_propios = spla.eigsh(MDF, k=eig, which='SM')
    #los valores propios que se sacan arriba son en realidad k**2, los convertimos 

    eigenvalues = np.sqrt(-valores_propios)
    return eigenvalues

A = finite_difference(20,10)
eigenvalues = encontrar_autovalores(A, 143) # k máximo que se le puede dar es N-1, donde N=(nx-2)*(ny-2), está especificado como print 
print(eigenvalues)
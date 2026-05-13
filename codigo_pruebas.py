import integ_method as im
import mascara as mask


# Parámetros de la simulación
Lx, Ly = 1.0, 1.0  # Tamaño del dominio
Nx, Ny = 150, 100    # Número de puntos en cada dirección
num_estados = 500    # Número de estados a calcular

# Crear la máscara y la matriz de diferencias finitas
mascara = mask.crear_mascara(Nx, Ny, formato='c', frontera=True)
matriz = im.finite_difference(mascara)

# Calcular los autovalores y autovectores
autovalores, autovectores = im.encontrar_autovalores(matriz, num_estados)

# Graficar la densidad de probabilidad para los últimos estados de mayor energía
im.plot_densidad_probabilidad(autovectores, mascara, 475)
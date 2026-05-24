import numpy as np
import simulacion_billar as sb
import matplotlib.pyplot as plt

mascara = sb.crear_mascara(170, 100, 'qc')
segmentos = sb.obtener_segmentos_contorno(mascara)

# The top wall is at y=98.5. The arc center is (70, 0).
# We want to hit the top wall at some x so that it bounces and passes through (70,0).
# Let's say it bounces at x=35.
# Point on top wall: P = (35, 98.5)
# Ray towards center: V = (70 - 35, 0 - 98.5) = (35, -98.5)
# We start slightly inside, along this ray.
O_inicial = np.array([35.0, 98.0]) # Just below the top wall
D_inicial = np.array([35.0, -98.5])
D_inicial = D_inicial / np.linalg.norm(D_inicial)

tray = sb.simular_trayectoria(O_inicial, D_inicial, segmentos, num_rebotes=10)
print(tray)

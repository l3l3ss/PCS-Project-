import numpy as np
import simulacion_billar as sb

mascara = sb.crear_mascara(170, 100, 'c')
segmentos = sb.obtener_segmentos_contorno(mascara)

O_inicial = np.array([85.0, 50.0])
dx = 162.61404449 - 85.0
dy = 76.15421978 - 50.0
ang = np.arctan2(dy, dx)
D_inicial = np.array([np.cos(ang), np.sin(ang)])

tray = sb.simular_trayectoria(O_inicial, D_inicial, segmentos, num_rebotes=10)
print(tray)

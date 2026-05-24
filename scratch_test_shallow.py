import numpy as np
import simulacion_billar as sb

mascara = sb.crear_mascara(170, 100, 'qc')
segmentos = sb.obtener_segmentos_contorno(mascara)

O_inicial = np.array([0.5, 10.0])
D_inicial = np.array([1.0, 0.0])

tray = sb.simular_trayectoria(O_inicial, D_inicial, segmentos, num_rebotes=10)
print(tray)

import numpy as np
import simulacion_billar as sb

# Parametros
O_inicial = np.array([5.0, 10.0]) # Try y=10.0 for more visible bouncing
D_inicial = np.array([1.0, 0.0])

mascara = sb.crear_mascara(170, 100, 'qc')
segmentos = sb.obtener_segmentos_contorno(mascara)

tray = sb.simular_trayectoria(O_inicial, D_inicial, segmentos, num_rebotes=10)
print(tray)

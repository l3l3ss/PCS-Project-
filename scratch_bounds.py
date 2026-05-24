import mascara as mask
import numpy as np
import matplotlib.pyplot as plt

mascara_c = mask.crear_mascara(170, 100, formato='c', frontera=True)
cs = plt.contour(mascara_c, levels=[0.5])
paths = cs.get_paths()
for p in paths:
    v = p.vertices
    print(f"Min X: {np.min(v[:,0])}, Max X: {np.max(v[:,0])}")
    print(f"Min Y: {np.min(v[:,1])}, Max Y: {np.max(v[:,1])}")

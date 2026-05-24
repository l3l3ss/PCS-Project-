import numpy as np

puntos_mono = np.array([
    [84.5, 49.5],
    [161.20, 75.13],
    [84.5, 98.5],
    [7.80, 75.13],
    [84.5, 49.5],
    [161.20, 23.87],
    [84.5, 0.5],
    [7.80, 23.87],
    [84.5, 49.5]
])

import matplotlib.pyplot as plt
import mascara as mask

mascara_mono = mask.crear_mascara(170, 100, 'c', frontera=True)
cs = plt.contour(mascara_mono, levels=[0.5])
paths = cs.get_paths()
for p in paths:
    v = p.vertices
    plt.plot(v[:,0], v[:,1], 'b-')

plt.plot(puntos_mono[:, 0], puntos_mono[:, 1], 'r-')
plt.savefig('test_mono.png')

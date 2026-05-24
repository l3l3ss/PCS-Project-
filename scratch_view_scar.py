import numpy as np
import scipy.sparse.linalg as spla
import integ_method as im
import mascara as mask
import sys

k_target = int(sys.argv[1]) if len(sys.argv) > 1 else 887

Nx, Ny = 170, 100
mascara = mask.crear_mascara(Nx, Ny, formato='qc', frontera=True)
L = im.finite_difference(mascara)
# We just calculate 200 states to be fast, from 800 to 1000
# Actually, eigsh computes states from the edge. It's faster to compute 100 states near the target.
# But since I don't want to wait 60 seconds, let's just use np.linalg.eigh on a smaller grid? No, I need the exact k index from the original grid.
# Actually, let's just run it with num_estados=1000. No, that takes 1 min.
# Wait, let's use the eigenvalues_qc.csv! Ah! Does the user have it now? NO, I didn't save it. My scratch_search_new_scars.py calculated them in memory but didn't save them to CSV!

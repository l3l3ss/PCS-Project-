import numpy as np
import simulacion_billar as sb

mascara = sb.crear_mascara(170, 100, 'qc')
segmentos = sb.obtener_segmentos_contorno(mascara)

def test_ray(O, D, num_rebotes):
    pos = sb.simular_trayectoria(O, D, segmentos, num_rebotes)
    if len(pos) < num_rebotes + 1:
        return False, pos
    return True, pos

# We want a V-shape. Let's start at the center of the top wall (x=35, y=98.5).
# Shoot towards the arc. We want it to hit the arc, bounce, and return to near (35, 98.5).
# Or maybe a "Bow-Tie" starting at the left wall (x=0.5, y=50.0).

best_dist = float('inf')
best_ang = None
best_pos = None

O_inicial = np.array([35.0, 98.0])

for ang_deg in np.linspace(-90, 0, 2000): # angles pointing right and down
    ang = np.radians(ang_deg)
    D = np.array([np.cos(ang), np.sin(ang)])
    
    success, pos = test_ray(O_inicial, D, num_rebotes=2)
    if success:
        # pos[0] is start, pos[1] is bounce 1, pos[2] is bounce 2 (return?)
        # For a V-shape, bounce 1 is arc, bounce 2 is back to top wall? No, bounce 2 should be back at origin!
        dist = np.linalg.norm(pos[2] - O_inicial)
        if dist < best_dist:
            best_dist = dist
            best_ang = ang_deg
            best_pos = pos

print(f"Mejor angulo para V-shape: {best_ang} deg, distancia retorno: {best_dist}")
print("Posiciones:", best_pos)

# What about a Bow-Tie? Starts at left wall x=1.0, y=50.0. 
# Bounces top wall, arc, bottom wall, left wall.
O_bowtie = np.array([1.0, 50.0])
best_dist_bt = float('inf')
best_ang_bt = None

for ang_deg in np.linspace(10, 80, 1000):
    ang = np.radians(ang_deg)
    D = np.array([np.cos(ang), np.sin(ang)])
    success, pos = test_ray(O_bowtie, D, num_rebotes=4)
    if success:
        # After 4 bounces, should be back at start
        dist = np.linalg.norm(pos[4] - O_bowtie)
        if dist < best_dist_bt:
            best_dist_bt = dist
            best_ang_bt = ang_deg

print(f"Mejor angulo para Bow-Tie: {best_ang_bt} deg, distancia retorno: {best_dist_bt}")


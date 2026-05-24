import numpy as np

def interseccion_rayo_segmento(O, D, A, B):
    v1 = O - A
    v2 = B - A
    v3 = np.array([-D[1], D[0]])
    dot = np.dot(v2, v3)
    if abs(dot) < 1e-10: return None, None
    t = np.cross(v2, v1) / dot
    u = np.dot(v1, v3) / dot
    if t > 1e-8 and 0 <= u <= 1: return t, u
    return None, None

def find_periodic():
    # Mask qc approx geometry
    nx, ny = 170, 100
    cx = 70
    radio = 99
    
    # We approximate the circle with segments
    theta = np.linspace(0, np.pi/2, 100)
    arc_points = np.column_stack((cx + radio*np.cos(theta), radio*np.sin(theta)))
    
    segmentos = []
    # Bottom: (0,0) to (cx+radio, 0)
    segmentos.append((np.array([0., 0.]), np.array([cx+radio, 0.])))
    # Left: (0,0) to (0, radio)
    segmentos.append((np.array([0., 0.]), np.array([0., radio])))
    # Top: (0, radio) to (cx, radio)
    segmentos.append((np.array([0., radio]), np.array([cx, radio])))
    
    # Arc
    for i in range(len(arc_points)-1):
        segmentos.append((arc_points[i], arc_points[i+1]))
        
    def simular(O, D, rebotes=3):
        pos = [O]
        for _ in range(rebotes):
            min_t = float('inf')
            mejor_int = None
            mejor_norm = None
            for A, B in segmentos:
                t, u = interseccion_rayo_segmento(O, D, A, B)
                if t is not None and t < min_t:
                    min_t = t
                    mejor_int = O + t*D
                    seg_vec = B - A
                    n = np.array([-seg_vec[1], seg_vec[0]])
                    n = n / np.linalg.norm(n)
                    if np.dot(D, n) > 0: n = -n
                    mejor_norm = n
            if mejor_int is not None:
                pos.append(mejor_int)
                D = D - 2*np.dot(D, mejor_norm)*mejor_norm
                O = mejor_int
            else:
                break
        return pos
    
    # Search for a ray starting at origin (0,0) that returns to origin after 3 bounces
    # Actually starting at origin is edge case. 
    # Let's start at bottom edge (x, 0) and shoot up/right.
    # It must bounce top, then arc, then return to (x, 0)
    best_dist = float('inf')
    best_x = 0
    best_ang = 0
    for x in np.linspace(10, 60, 50):
        for ang in np.linspace(0.1, np.pi/2 - 0.1, 100):
            O = np.array([x, 0.0])
            D = np.array([np.cos(ang), np.sin(ang)])
            pos = simular(O, D, rebotes=4)
            if len(pos) >= 4:
                # distance from 4th point to start
                dist = np.linalg.norm(pos[3] - O)
                if dist < best_dist:
                    best_dist = dist
                    best_x = x
                    best_ang = ang
    print(f"Mejor triangulo: x={best_x}, ang={best_ang*180/np.pi} deg, error={best_dist}")
    
find_periodic()

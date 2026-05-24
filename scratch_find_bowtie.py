import numpy as np
from scipy.optimize import root_scalar

def reflection_error(theta):
    # theta in radians
    P = np.array([120 + 50 * np.cos(theta), 50 + 50 * np.sin(theta)])
    v_in = P - np.array([85.0, 50.0])
    v_out = np.array([85.0, 0.0]) - P
    
    u = -v_in / np.linalg.norm(v_in)
    w = v_out / np.linalg.norm(v_out)
    
    bisector = u + w
    # normal
    n = np.array([np.cos(theta), np.sin(theta)])
    
    # cross product should be 0
    return bisector[0]*n[1] - bisector[1]*n[0]

res = root_scalar(reflection_error, bracket=[0.01, np.pi/2])
theta = res.root
P = np.array([120 + 50 * np.cos(theta), 50 + 50 * np.sin(theta)])

print(f"theta_rad = {theta}")
print(f"P = {P}")
v_out = np.array([85.0, 0.0]) - P
# angle from bottom center (85, 0) to P
v_from_bottom = P - np.array([85.0, 0.0])
angle_from_bottom = np.arctan2(v_from_bottom[1], v_from_bottom[0])
print(f"angle_from_bottom = {angle_from_bottom}")

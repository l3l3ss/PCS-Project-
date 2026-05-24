import numpy as np
import matplotlib.pyplot as plt
from mascara import crear_mascara

def obtener_segmentos_contorno(mascara):
    """
    Extrae los segmentos de línea que forman el contorno de la máscara binaria.
    Utiliza matplotlib.contour para encontrar el polígono de frontera.
    """
    # Usar una figura temporal que no se mostrará
    fig, ax = plt.subplots()
    # contour asume que el primer eje de mascara es Y y el segundo es X.
    cs = ax.contour(mascara, levels=[0.5])
    
    segmentos = []
    # allsegs contiene los segmentos para cada nivel.
    # Como solo usamos el nivel 0.5, extraemos sus polígonos.
    for poligonos_nivel in cs.allsegs:
        for v in poligonos_nivel:
            for i in range(len(v)-1):
                segmentos.append((v[i], v[i+1]))
            # Cerrar el polígono si los extremos no coinciden
            if len(v) > 0 and not np.allclose(v[0], v[-1]):
                segmentos.append((v[-1], v[0]))
    
    plt.close(fig)
    return segmentos

def interseccion_rayo_segmento(O, D, A, B):
    """
    Encuentra la intersección entre un rayo O + t*D y un segmento AB.
    Devuelve t (distancia a lo largo del rayo) y u (parámetro a lo largo del segmento).
    """
    v1 = O - A
    v2 = B - A
    v3 = np.array([-D[1], D[0]])
    
    dot = np.dot(v2, v3)
    if abs(dot) < 1e-10:
        return None, None # Paralelos
    
    t = np.cross(v2, v1) / dot
    u = np.dot(v1, v3) / dot
    
    # Tolerancia epsilon (1e-8) para evitar auto-intersecciones en el rebote
    if t > 1e-8 and 0 <= u <= 1:
        return t, u
    return None, None

def simular_trayectoria(O_inicial, D_inicial, segmentos, num_rebotes=30):
    """
    Simula la trayectoria de una partícula en el billar rebotando
    especularmente en los segmentos del contorno.
    """
    posiciones = [O_inicial]
    O = O_inicial.copy()
    D = D_inicial.copy()
    D = D / np.linalg.norm(D)
    
    for _ in range(num_rebotes):
        min_t = float('inf')
        mejor_interseccion = None
        mejor_normal = None
        
        # Encontrar la primera intersección con cualquier segmento
        for A, B in segmentos:
            t, u = interseccion_rayo_segmento(O, D, A, B)
            if t is not None and t < min_t:
                min_t = t
                mejor_interseccion = O + t * D
                
                # Calcular normal del segmento
                seg_vec = B - A
                n = np.array([-seg_vec[1], seg_vec[0]])
                n = n / np.linalg.norm(n)
                
                # La normal debe apuntar hacia donde viene el rayo (reflexión)
                if np.dot(D, n) > 0:
                    n = -n
                mejor_normal = n
                
        if mejor_interseccion is not None:
            posiciones.append(mejor_interseccion)
            # Ley de reflexión: V_reflejado = V_incidente - 2(V_incidente . n)n
            D = D - 2 * np.dot(D, mejor_normal) * mejor_normal
            D = D / np.linalg.norm(D)
            O = mejor_interseccion
        else:
            # Si se "escapa" (no debería ocurrir en máscara cerrada)
            print("Partícula escapada del billar.")
            # Añadir un paso final para visualizar dónde escapó
            posiciones.append(O + D * 10)
            break
            
    return np.array(posiciones)

def visualizar_caos(tipo_mascara='c', nx=200, ny=100, num_trayectorias=3, 
                   rebotes=30, variacion_angular=0.005, angulo_base=None, O_inicial=None):
    """
    Configura y lanza múltiples trayectorias con pequeña variación en las
    condiciones iniciales, dibujándolas sobre la máscara seleccionada.
    """
    # Estilo oscuro y moderno
    plt.style.use('dark_background')
    
    # 1. Crear la máscara a partir de mascara.py
    mascara = crear_mascara(nx, ny, tipo_mascara)
    
    # 2. Extraer el contorno geométrico para detectar colisiones
    segmentos = obtener_segmentos_contorno(mascara)
    
    # 3. Definir posición inicial y ángulo si no se dan
    if O_inicial is None:
        Y_idx, X_idx = np.where(mascara)
        if len(Y_idx) == 0:
            raise ValueError("La máscara está vacía, no hay espacio para simular.")
        
        # Desplazado a la izquierda (20% del ancho) y asimétrico en Y (33% de la altura)
        # Esto destruye deliberadamente las simetrías centrales que causan órbitas periódicas
        x_start = np.min(X_idx) + (np.max(X_idx) - np.min(X_idx)) * 0.2
        y_start = np.min(Y_idx) + (np.max(Y_idx) - np.min(Y_idx)) * 0.33
        O_inicial = np.array([x_start, y_start])
        
    if angulo_base is None:
        # Ángulo totalmente aleatorio en cada simulación
        angulo_base = np.random.uniform(0, 2 * np.pi)
    
    # Configurar figura premium
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('#0b0c10')
    ax.set_facecolor('#0b0c10')
    
    # Dibujar la mesa de billar con suavizado (contour/contourf) en vez del pixelado
    # Fondo de la mesa (gris azulado oscuro)
    ax.contourf(mascara, levels=[0.5, 1.5], colors=['#1f2833'])
    # Borde de la mesa brillante
    ax.contour(mascara, levels=[0.5], colors=['#45a29e'], linewidths=2.5)

    # Colores brillantes para las trayectorias (Cyan, Magenta fluorescente, Verde lima, etc)
    colores_neon = ['#66fcf1', '#ff007f', '#39ff14', '#fce803', '#bf00ff']
    
    # 4. Lanzar las diferentes trayectorias
    for i in range(num_trayectorias):
        angulo = angulo_base + (i - num_trayectorias//2) * variacion_angular
        D_inicial = np.array([np.cos(angulo), np.sin(angulo)])
        
        tray = simular_trayectoria(O_inicial, D_inicial, segmentos, rebotes)
        
        if len(tray) > 0:
            color = colores_neon[i % len(colores_neon)]
            etiqueta = rf"$\Delta\theta = {(i - num_trayectorias//2)*variacion_angular:+.3f}$ rad"
            
            # Efecto Resplandor (Glow) usando líneas superpuestas
            ax.plot(tray[:, 0], tray[:, 1], color=color, alpha=0.15, linewidth=7)
            ax.plot(tray[:, 0], tray[:, 1], color=color, alpha=0.3, linewidth=4)
            # Línea central nítida
            ax.plot(tray[:, 0], tray[:, 1], color=color, alpha=0.9, linewidth=1.5, label=etiqueta)
            
            # Marcar el punto final
            ax.scatter(tray[-1, 0], tray[-1, 1], color=color, s=70, edgecolor='white', linewidth=1.2, zorder=4)
            
    # Marcar el punto de inicio con una estrella brillante
    ax.scatter(O_inicial[0], O_inicial[1], color='white', s=150, marker='*', 
               edgecolor='#ff007f', linewidth=1.5, zorder=5, label='Inicio')
            
    # Títulos y limpieza de ejes
    fig.suptitle(f"Simulación de Caos: Billar '{tipo_mascara}'", color='white', fontsize=18, fontweight='bold', y=0.96)
    ax.set_title(f"{rebotes} rebotes", color='#c5c6c7', fontsize=12, pad=10)
    ax.axis('off') # Quita el feo recuadro y los números de los ejes
    ax.set_aspect('equal')
    
    # Leyenda estilizada
    legend = ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, 
                       facecolor='#1f2833', edgecolor='#45a29e', fontsize=11, labelcolor='white')
    legend.get_frame().set_alpha(0.9)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # -------------------------------------------------------------
    # EJEMPLOS DE USO: DESCOMENTA EL QUE QUIERAS VER
    # -------------------------------------------------------------
    
    # 1. Estadio de Bunimovich ('c') -> CAÓTICO
    # Las trayectorias se separan exponencialmente en el espacio de fases
    # print("Simulando Estadio de Bunimovich (Caótico)...")
    # visualizar_caos(tipo_mascara='qc', nx=1000, ny=750, num_trayectorias=1, rebotes=50, variacion_angular=0.01)

    
    # 2. Billar rectangular ('r') -> NO CAÓTICO (Integrable)
    # Las trayectorias se mantienen relativamente cerca (divergencia lineal/polinómica)
    # print("\nSimulando Billar Rectangular (Integrable)...")
    # visualizar_caos(tipo_mascara='r', num_trayectorias=3, rebotes=25, variacion_angular=0.005)
    
    # 3. Billar cuarto de estadio ('qc') -> CAÓTICO
    # print("\nSimulando Cuarto de Estadio (Caótico)...")
    # visualizar_caos(tipo_mascara='qc', num_trayectorias=3, rebotes=25, variacion_angular=0.005)

    # -------------------------------------------------------------
    # 4. CICATRIZ CUÁNTICA: Órbita Periódica (Rebote Vertical)
    # -------------------------------------------------------------
    # Esta es la trayectoria clásica exacta que genera las famosas "cicatrices"
    # Prueba con los estados de alta localización como k=848 o k=985.
    # print("\nSimulando Órbita Periódica (Cicatriz Cuántica - Rebote Vertical)...")
    # punto_inicio_cicatriz = np.array([35.0, 50.0]) 
    # angulo_arriba = np.pi / 2
    # visualizar_caos(tipo_mascara='qc', nx=170, ny=100, num_trayectorias=1, rebotes=50, 
    #                 variacion_angular=0.0, angulo_base=angulo_arriba, O_inicial=punto_inicio_cicatriz)
                    
    # -------------------------------------------------------------
    # 5. CICATRIZ CUÁNTICA 2: Órbita Periódica (Rebote Horizontal en la base)
    # -------------------------------------------------------------
    # Esta trayectoria corresponde a estados hiper-localizados cerca de la base,
    # como los que ocurren en k=805 o k=868 (Galería de Susurros recta).
    print("\nSimulando Órbita Periódica (Cicatriz Cuántica - Rebote Horizontal)...")
    
    # IMPORTANTE: Empezar en x=5.0 para estar dentro de la frontera (que empieza en x=0.5)
    punto_inicio_h = np.array([5.0, 1.0]) 
    angulo_horizontal = 0.0  # 0 grados exactos (hacia la derecha)
    
    visualizar_caos(tipo_mascara='qc', nx=170, ny=100, num_trayectorias=1, rebotes=100, 
                    variacion_angular=0.0, angulo_base=angulo_horizontal, O_inicial=punto_inicio_h)

import matplotlib.pyplot as plt
import numpy as np
import mascara as masc
import integ_method as integ

def plot_distribucion_espaciado(espaciados, bins=100, title="Distribución de espaciado entre autovalores"):
    """
    Visualiza la distribución del espaciado entre autovalores usando un histograma.
    También superpone las distribuciones teóricas de Poisson (sistemas integrables) 
    y Wigner (sistemas caóticos - GOE) para comparar.
    
    Parámetros:
    - espaciados: array o lista con las diferencias entre autovalores consecutivos.
    - bins: número de contenedores para el histograma.
    - title: título del gráfico.
    """
    plt.figure(figsize=(8, 6))
    
    # Normalizamos el espaciado dividiendo por la media (práctica estándar en caos cuántico)
    # para que s = S / <S>
    mean_espaciado = np.mean(espaciados)
    if mean_espaciado == 0:
        print("Advertencia: El espaciado medio es 0.")
        s = espaciados
    else:
        s = espaciados / mean_espaciado
    
    # Histograma de los datos numéricos
    plt.hist(s, bins=bins, density=True, alpha=0.7, color='royalblue', edgecolor='black', label='Espaciado numérico')
    
    # Rango de s para graficar las distribuciones teóricas
    s_vals = np.linspace(0, np.max(s) + 0.5, 200)
    
    # Distribución de Poisson (sistemas regulares / integrables)
    poisson = np.exp(-s_vals)
    
    # Distribución de Wigner (GOE, sistemas caóticos con simetría de inversión temporal)
    wigner = (np.pi / 2) * s_vals * np.exp(-np.pi * s_vals**2 / 4)
    
    # Trazar curvas teóricas
    plt.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable)')
    plt.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Caótico)')
    
    plt.title(title, fontsize=14)
    plt.xlabel('Espaciado normalizado ($s = S / \\langle S \\rangle$)', fontsize=12)
    plt.ylabel('Densidad de probabilidad $P(s)$', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Ejemplo de uso (puedes reemplazar esto con tus datos reales)
    # autovalores = np.loadtxt("autovalores.txt") # O cargar desde tu cálculo
    
    mascara = masc.crear_mascara(100, 50, formato='qc')
    matrizA = integ.finite_difference(mascara)
    autovalores = integ.encontrar_autovalores(matrizA, 500)
    espaciados = np.diff(autovalores)

    plot_distribucion_espaciado(espaciados)
import matplotlib.pyplot as plt
import numpy as np
import mascara as masc
import integ_method as integ
import bem_method as bem

def plot_distribucion_espaciado(espaciados, formato=None, bins=100):
    """
    Visualiza la distribución del espaciado entre autovalores usando un histograma.
    Dependiendo del formato de la máscara elegida, superpone la distribución 
    teórica de Poisson o de Wigner.
    
    Parámetros:
    - espaciados: array o lista con las diferencias entre autovalores consecutivos.
    - formato: 'r' (rectangular), 'c' (estadio) para Poisson, o 'qc' (cuarto de estadio) para Wigner.
    - bins: número de contenedores para el histograma.
    """
    plt.figure(figsize=(8, 6))
    title=f"Distribución de espaciado entre autovalores, formato={formato}"
    
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
    
    # Trazar curvas teóricas dependiendo del formato
    if formato in ['r', 'c']:
        plt.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable / Simetrías)')
    elif formato == 'qc':
        plt.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Caótico)')
    else:
        # Si no se especifica o es otro formato, graficamos ambas
        plt.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable)')
        plt.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Caótico)')
    
    plt.title(title, fontsize=14)
    plt.xlabel('Espaciado normalizado ($s = S / \\langle S \\rangle$)', fontsize=12)
    plt.ylabel('Densidad de probabilidad $P(s)$', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    #plt.savefig(f"output/distribucion_espaciado_{formato_elegido}_nNormalizar.png")
    plt.show()
    plt.close()


if __name__ == "__main__":
    # Ejemplo de uso (puedes reemplazar esto con tus datos reales)
    # autovalores = np.loadtxt("autovalores.txt") # O cargar desde tu cálculo

    formatos = ['r', 'c', 'qc']

    for formato_elegido in formatos:
        mascara = masc.crear_mascara(200, 100, formato=formato_elegido)
        matrizA = integ.finite_difference(mascara)
        autovalores = integ.encontrar_autovalores(matrizA, 1000)
        espaciados = np.diff(autovalores)

        plot_distribucion_espaciado(espaciados, formato=formato_elegido)
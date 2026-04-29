import matplotlib.pyplot as plt
import numpy as np
import mascara as masc
import integ_method as integ

def plot_distribucion_espaciado(espaciados, formato=None, bins=100, mostrar_mascara=True, mascara=None):
    """
    Visualiza la distribución del espaciado entre autovalores usando un histograma.
    Dependiendo del formato de la máscara elegida, superpone la distribución 
    teórica de Poisson o de Wigner.
    
    Parámetros:
    - espaciados: array o lista con las diferencias entre autovalores consecutivos.
    - formato: 'r' (rectangular), 'c' (estadio) para Poisson, o 'qc' (cuarto de estadio) para Wigner.
    - bins: número de contenedores para el histograma.
    """
    if mostrar_mascara and mascara is None and formato is not None:
        try:
            mascara = masc.crear_mascara(60, 50, formato=formato)
        except Exception:
            mascara = None

    if mascara is not None:
        fig, (ax_dist, ax_mask) = plt.subplots(
            1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [3, 1]}
        )
    else:
        fig, ax_dist = plt.subplots(figsize=(8, 6))
        ax_mask = None

    title = f"Distribución de espaciado entre autovalores, formato={formato}"
    
    # Normalizamos el espaciado dividiendo por la media (práctica estándar en caos cuántico)
    # para que s = S / <S>
    mean_espaciado = np.mean(espaciados)
    if mean_espaciado == 0:
        print("Advertencia: El espaciado medio es 0.")
        s = espaciados
    else:
        s = espaciados / mean_espaciado
    
    # Histograma de los datos numéricos
    ax_dist.hist(s, bins=bins, density=True, alpha=0.7, color='royalblue', edgecolor='black', label='Espaciado numérico')
    
    # Rango de s para graficar las distribuciones teóricas
    s_vals = np.linspace(0, np.max(s) + 0.5, 200)
    
    # Distribución de Poisson (sistemas regulares / integrables)
    poisson = np.exp(-s_vals)
    
    # Distribución de Wigner (GOE, sistemas caóticos con simetría de inversión temporal)
    wigner = (np.pi / 2) * s_vals * np.exp(-np.pi * s_vals**2 / 4)
    
    # Trazar curvas teóricas dependiendo del formato
    if formato in ['r', 'c']:
        ax_dist.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable / Simetrías)')
    elif formato == 'qc':
        ax_dist.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Caótico)')
    else:
        # Si no se especifica o es otro formato, graficamos ambas
        ax_dist.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable)')
        ax_dist.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Caótico)')
    
    ax_dist.set_title(title, fontsize=14)
    ax_dist.set_xlabel('Espaciado normalizado ($s = S / \\langle S \\rangle$)', fontsize=12)
    ax_dist.set_ylabel('Densidad de probabilidad $P(s)$', fontsize=12)
    ax_dist.legend(fontsize=11)
    ax_dist.grid(True, linestyle='--', alpha=0.6)

    if ax_mask is not None:
        ax_mask.imshow(mascara, cmap='gray_r', interpolation='nearest')
        ax_mask.set_title('Forma de la máscara', fontsize=12)
        ax_mask.axis('off')

    fig.tight_layout()
    #plt.savefig(f"output/distribucion_espaciado_{formato_elegido}.png")
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    # Ejemplo de uso (puedes reemplazar esto con tus datos reales)
    # autovalores = np.loadtxt("autovalores.txt") # O cargar desde tu cálculo

    formatos = ['c']

    for formato_elegido in formatos:
        mascara = masc.crear_mascara(60, 50, formato=formato_elegido)
        matrizA = integ.finite_difference(mascara)
        autovalores = integ.encontrar_autovalores(matrizA, 1000)
        espaciados = np.diff(autovalores)

        plot_distribucion_espaciado(espaciados, formato=formato_elegido)
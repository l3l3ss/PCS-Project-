import matplotlib.pyplot as plt
import numpy as np
import mascara as masc
import integ_method as integ

def plot_distribucion_espaciado(espaciados, mascara, formato=None, bins=100):
    """
    Visualiza la distribución del espaciado entre autovalores usando un histograma.
    Dependiendo del formato de la máscara elegida, superpone la distribución 
    teórica de Poisson o de Wigner. También muestra la forma de la máscara.
    
    Parámetros:
    - espaciados: array o lista con las diferencias entre autovalores consecutivos.
    - mascara: matriz booleana que representa la forma del billar.
    - formato: 'r' (rectangular) para Poisson,'c' (estadio) para Wigner
    - bins: número de contenedores para el histograma.
    """
    from matplotlib.colors import ListedColormap
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1, 2]})
    title = f"Análisis espectral y geometría, formato={formato}"
    fig.suptitle(title, fontsize=16)
    
    # 1. Plot de la máscara en la izquierda
    cmap_personalizado = ListedColormap(['red', 'blue'])
    ax1.imshow(mascara, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    ax1.set_title("Geometría de la Máscara", fontsize=14)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    
    # 2. Plot de la distribución en la derecha
    # Normalizamos el espaciado dividiendo por la media 
    # para que s = S / <S>
    mean_espaciado = np.mean(espaciados)
    if mean_espaciado == 0:
        print("Advertencia: El espaciado medio es 0.")
        s = espaciados
    else:
        s = espaciados / mean_espaciado     
    
    # Histograma de los datos numéricos
    ax2.hist(s, bins=bins, density=True, alpha=0.7, color='royalblue', edgecolor='black', label='Espaciado numérico')
    
    # Rango de s para graficar las distribuciones teóricas
    s_vals = np.linspace(0, np.max(s) + 0.5, 200)
    
    # Distribución de Poisson 
    poisson = np.exp(-s_vals)
    
    # Distribución de Wigner 
    wigner = (np.pi / 2) * s_vals * np.exp(-np.pi * s_vals**2 / 4)
    
    # Trazar curvas teóricas dependiendo del formato
    if formato in ['r', 'c']:
        ax2.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable / Simetrías)')
    elif formato =='qc':
        ax2.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Caótico)')
    else:
        # Si no se especifica o es otro formato, graficamos ambas
        ax2.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable)')
        ax2.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Caótico)')
    
    ax2.set_title("Distribución de espaciado entre autovalores", fontsize=14)
    ax2.set_xlabel('Espaciado normalizado ($s = S / \\langle S \\rangle$)', fontsize=12)
    ax2.set_ylabel('Densidad de probabilidad $P(s)$', fontsize=12)
    ax2.legend(fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    #plt.savefig(f"output/distribucion_espaciado_{formato}_nNormalizar.png")
    plt.show()
    plt.close()


if __name__ == "__main__":

    formatos = ['c']

    for formato_elegido in formatos:
        mascara = masc.crear_mascara(170, 100, formato=formato_elegido)
        matrizA = integ.finite_difference(mascara)
        autovalores, autovectores = integ.encontrar_autovalores(matrizA, 1000)
        espaciados = np.diff(autovalores)

        plot_distribucion_espaciado(espaciados, mascara, formato=formato_elegido, bins=100)
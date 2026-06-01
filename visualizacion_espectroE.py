import matplotlib.pyplot as plt
import numpy as np
import mascara as masc
import integ_method as integ

def plot_distribucion_espaciado(espaciados, mascara, formato=None, bins=70):
    from matplotlib.colors import ListedColormap

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1, 2]})
    title = f"Spectral analysis and geometry"
    fig.suptitle(title, fontsize=16)

    # --- PANEL 1: GEOMETRÍA ---
    cmap_personalizado = ListedColormap(['red', 'blue'])
    ax1.imshow(mascara, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    ax1.set_title("Mascara geometry", fontsize=14)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')

    # --- NORMALIZACIÓN DEL ESPACIADO ---
    mean_espaciado = np.mean(espaciados)
    if mean_espaciado == 0:
        print("Advertencia: El espaciado medio es 0.")
        s = espaciados
    else:
        s = espaciados / mean_espaciado     

    # --- PANEL 2: HISTOGRAMA NUMÉRICO CON BARRAS DE ERROR ---
    # 1. Calcular el histograma con NumPy
    counts, bin_edges = np.histogram(s, bins=bins)
    total_datos = len(s)
    bin_widths = np.diff(bin_edges)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # 2. Normalizar a densidad de probabilidad
    p_densidad = counts / (total_datos * bin_widths)

    # 3. Calcular errores (Poisson) y propagarlos
    error_conteos = 2*np.sqrt(counts)
    error_densidad = error_conteos / (total_datos * bin_widths)

    # 4. Graficar barras con yerr y capsize
    ax2.bar(bin_centers, p_densidad, width=bin_widths, alpha=0.7, color='royalblue', 
            edgecolor='black', label='Espaciado numérico', yerr=error_densidad, capsize=3)

    # --- CURVAS TEÓRICAS ---
    s_vals = np.linspace(0, np.max(s) + 0.5, 200)
    poisson = np.exp(-s_vals)
    wigner = (np.pi / 2) * s_vals * np.exp(-np.pi * s_vals**2 / 4)

    if formato in ['r', 'c']:
        ax2.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable)')
    elif formato == 'qc':
        ax2.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Chaotic)')
    else:
        ax2.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable)')
        ax2.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Chaotic)')

    # --- FORMATO FINAL ---
    ax2.set_title("Spacing distribution", fontsize=14)
    ax2.set_xlabel('Normalized spacing ($s = S / \\langle S \\rangle$)', fontsize=12)
    ax2.set_ylabel('$P(s)$', fontsize=12)
    ax2.legend(fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()
    plt.close()

if __name__ == "__main__":
    formatos = ['r']

    for formato_elegido in formatos:
        mascara = masc.crear_mascara(170, 100, formato=formato_elegido)
        matrizA = integ.finite_difference(mascara)
        autovalores, autovectores = integ.encontrar_autovalores(matrizA, 2000)
        espaciados = np.diff(autovalores)

        plot_distribucion_espaciado(espaciados, mascara, formato=formato_elegido, bins=35)
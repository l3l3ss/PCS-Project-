import matplotlib.pyplot as plt
import numpy as np
import mascara as masc
import integ_method as integ

def plot_distribucion_espaciado(espaciados, mascara, formato=None, bins=100):
    from matplotlib.colors import ListedColormap

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1, 2]})
    title = f"Análisis espectral y geometría, formato={formato}"
    fig.suptitle(title, fontsize=16)

    cmap_personalizado = ListedColormap(['red', 'blue'])
    ax1.imshow(mascara, cmap=cmap_personalizado, origin='lower', vmin=0, vmax=1)
    ax1.set_title("Geometría de la Máscara", fontsize=14)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')

    mean_espaciado = np.mean(espaciados)
    if mean_espaciado == 0:
        print("Advertencia: El espaciado medio es 0.")
        s = espaciados
    else:
        s = espaciados / mean_espaciado     

    ax2.hist(s, bins=bins, density=True, alpha=0.7, color='royalblue', edgecolor='black', label='Espaciado numérico')

    s_vals = np.linspace(0, np.max(s) + 0.5, 200)

    poisson = np.exp(-s_vals)

    wigner = (np.pi / 2) * s_vals * np.exp(-np.pi * s_vals**2 / 4)

    if formato in ['r', 'c']:
        ax2.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable / Simetrías)')
    elif formato =='qc':
        ax2.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Caótico)')
    else:

        ax2.plot(s_vals, poisson, 'r--', linewidth=2, label='Poisson (Integrable)')
        ax2.plot(s_vals, wigner, 'g-', linewidth=2, label='Wigner GOE (Caótico)')

    ax2.set_title("Distribución de espaciado entre autovalores", fontsize=14)
    ax2.set_xlabel('Espaciado normalizado ($s = S / \\langle S \\rangle$)', fontsize=12)
    ax2.set_ylabel('Densidad de probabilidad $P(s)$', fontsize=12)
    ax2.legend(fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    plt.show()
    plt.close()

if __name__ == "__main__":

    formatos = ['qc']

    for formato_elegido in formatos:
        mascara = masc.crear_mascara(170, 100, formato=formato_elegido)
        matrizA = integ.finite_difference(mascara)
        autovalores, autovectores = integ.encontrar_autovalores(matrizA, 1500)
        espaciados = np.diff(autovalores)

        plot_distribucion_espaciado(espaciados, mascara, formato=formato_elegido, bins=25)
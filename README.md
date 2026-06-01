# Quantum Chaos and the Statistics of Energy Levels

This project explores how classical chaos shows up in quantum mechanics by studying the statistical properties of energy spectra in 2D billiards. We solve the time-independent Schrödinger equation numerically and compare two systems with completely different classical dynamics: a rectangular billiard (integrable) and a Bunimovich stadium billiard (chaotic).

The main result is a numerical verification of the **Bohigas-Giannoni-Schmit (BGS) conjecture**: the energy level spacings of a classically chaotic system follow the Wigner-Dyson distribution, while those of an integrable system follow a Poisson distribution.

This is the code for the *Physics of Complex Systems* project at the Universidad de Granada (Physics Degree, 2026).

---

## How it works

We discretize the 2D domain using a finite difference method (FDM) and impose Dirichlet boundary conditions (the wavefunction vanishes at the walls). The Hamiltonian becomes a large sparse matrix, which we diagonalize with `scipy` to get the eigenvalues and eigenvectors.

Three billiard geometries are supported:

| Code | Shape | Classical dynamics |
|------|-------|--------------------|
| `'r'` | Rectangle | Integrable → Poisson |
| `'c'` | Full stadium | Mixed (symmetry issue) |
| `'qc'` | Quarter-stadium | Chaotic → Wigner-Dyson |

> **Why the quarter-stadium?** The full stadium has two mirror symmetries (x and y axes), which splits the spectrum into four independent subsystems. When combined, they produce a near-Poisson distribution even though the system is chaotic. By taking just one quarter, we break those symmetries and recover the clean Wigner-Dyson statistics.

---

## Repository structure

```
PCS-Project/
│
├── mascara.py                  # Generates the billiard geometry masks
├── integ_method.py             # FDM matrix builder + eigenvalue solver + density plotter
├── visualizacion_espectroE.py  # Spacing distribution histogram + theoretical curves
├── dens_probabilidad.py        # Probability density visualizer (2D heatmap + 3D surface)
│
├── output/                     # Saved eigenvalue CSV files (auto-generated, can be large)
├── docs/                       # Project report (PDF)
└── presentation/               # Slides
```

---

## Requirements

You need Python 3 and the following libraries:

```
numpy
scipy
matplotlib
pandas
```

Install them all at once with:

```bash
pip install numpy scipy matplotlib pandas
```

---

## Usage

### 1. Spectral analysis — spacing distribution

This is the main script. It builds the FDM matrix, computes eigenvalues, and plots the normalized spacing histogram against the Poisson and Wigner-Dyson theoretical curves.

```bash
python visualizacion_espectroE.py
```

To change the geometry, open the file and edit this line near the bottom:

```python
formatos = ['r']   # options: 'r' (rectangle), 'c' (full stadium), 'qc' (quarter-stadium)
```

You can also run multiple geometries at once:

```python
formatos = ['r', 'c', 'qc']
```

The grid size is fixed at **170×100** and we compute **2000 eigenvalues** by default. Larger grids give more accurate results but take longer.

---

### 2. Probability density of eigenstates

This script plots the probability density |ψ(x,y)|² for a specific eigenstate — both as a 2D heatmap and a 3D surface. This is how we visualize **quantum scars**.

```bash
python dens_probabilidad.py
```

To change which eigenstate to plot or which geometry to use, edit these lines:

```python
formato = 'c'         # geometry: 'r', 'c', or 'qc'
num_estados = 2000    # number of eigenstates to compute
# ...
im.plot_densidad_probabilidad(autovectores, mascara, 1400)  # plot eigenvector 1400
```

The first time you run this, the eigenvectors are computed and saved to `output/eigenvalues_<formato>.csv`. On subsequent runs, the file is loaded directly — so it's much faster.

---

### 3. Geometry preview

To quickly visualize the three masks:

```bash
python mascara.py
```

This shows the rectangular, full-stadium, and quarter-stadium grids side by side.

---

## What to expect

**Spacing distribution for the rectangle (`'r'`):** the histogram peaks at s=0 and decays exponentially — a Poisson distribution. Energy levels are uncorrelated and can be arbitrarily close.

**Spacing distribution for the quarter-stadium (`'qc'`):** the histogram peaks around s≈1 and goes to zero at s=0 — a Wigner-Dyson distribution. Energy levels repel each other.

**Probability density for high-energy states of the stadium:** most states look roughly uniform (quantum ergodicity), but some show **quantum scars** — clear concentration of |ψ|² along specific curves that correspond to unstable periodic orbits of the classical billiard.

---

## Authors

María de los Ángeles Lara Consuegra & Pablo Orellana Chornyak  
Universidad de Granada — Facultad de Ciencias, 2026
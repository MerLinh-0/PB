import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def f(x, y):
    return (x - 10)**2 + (x*y - 50000)**2

# Siatka wartości x1 (od 0 do 20) i x2 (od 0 do 10000)
x = np.linspace(0.1, 20, 400)
y = np.linspace(0, 10000, 400)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# Konfiguracja głównego okna
fig = plt.figure(figsize=(15, 6))

# --- Wykres 1: Widok 3D ---
ax1 = fig.add_subplot(121, projection='3d')
# Używamy logarytmu dla Z, żeby "wypłaszczyć" gigantyczne ściany i pokazać wąwóz
surf = ax1.plot_surface(X, Y, np.log10(Z + 1), cmap='viridis', edgecolor='none', alpha=0.9)
ax1.set_title("Wizualizacja 3D wąwozu (Skala logarytmiczna Z)")
ax1.set_xlabel("X (x1)")
ax1.set_ylabel("Y (x2)")
ax1.set_zlabel("log10(f(x))")
# Widok lekko z góry
ax1.view_init(elev=40, azim=-60)

# --- Wykres 2: Mapa poziomicowa (Kontury z góry) ---
ax2 = fig.add_subplot(122)
# LogNorm pozwala ładnie pokolorować rzędy wielkości
cont = ax2.contourf(X, Y, Z, norm=LogNorm(vmin=1, vmax=Z.max()), cmap='viridis', levels=50)
plt.colorbar(cont, ax=ax2, label="Wartość funkcji f(x,y)")

# Zaznaczamy kluczowe punkty
ax2.plot(10, 5000, 'r*', markersize=15, label="Minimum (10, 5000)")
ax2.plot(0, 0, 'wo', markersize=8, markeredgecolor='k', label="Stary Start [0, 0]")
ax2.plot(10, 4900, 'yo', markersize=8, markeredgecolor='k', label="Nowy Start [10, 4900]")

ax2.set_title("Poziomice (widok z góry)")
ax2.set_xlabel("X (x1)")
ax2.set_ylabel("Y (x2)")
ax2.legend()

plt.tight_layout()
plt.show()
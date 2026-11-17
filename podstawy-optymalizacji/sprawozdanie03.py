import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import warnings

# Wyłączenie pomniejszych ostrzeżeń o precyzji zmiennoprzecinkowej z głębi SciPy
warnings.filterwarnings("ignore", category=RuntimeWarning)

# 1. Definicja funkcji celu
def f(vars):
    x, y = vars
    return (1 - x)**2 + 22 * (y - x**2)**2

# 2. Definicje ograniczeń g_j(x, y) <= 0
def g1(vars): return 2 - vars[1]           # 2 - y <= 0
def g2(vars): return vars[0] + 2           # x + 2 <= 0
def g3(vars): return vars[1] - vars[0] - 6 # y - x - 6 <= 0

# 3. Zewnętrzna funkcja kary
def zewnetrzna_funkcja_kary(vars, rho):
    kara = max(0, g1(vars))**2 + max(0, g2(vars))**2 + max(0, g3(vars))**2
    return f(vars) + rho * kara

# 4. Wewnętrzna funkcja kary (POPRAWIONA)
def wewnetrzna_funkcja_kary(vars, rho):
    # Margines 1e-6 zapobiega dzieleniu przez zera na samej krawędzi, 
    # a 1e12 (zamiast np.inf) zapobiega błędom numdiff przy badaniu gradientu
    if g1(vars) >= -1e-6 or g2(vars) >= -1e-6 or g3(vars) >= -1e-6:
        return 1e12
    
    kara = (-1.0 / g1(vars)) + (-1.0 / g2(vars)) + (-1.0 / g3(vars))
    return f(vars) + rho * kara

# --- ALGORYTM GŁÓWNY ---
def optymalizuj(metoda_kary, metoda_podrzedna, punkt_startowy, zewnetrzna=True):
    x_current = np.array(punkt_startowy)
    
    rho = 1.0 if zewnetrzna else 10.0
    alpha_zewn = 2.0
    alpha_wewn = 0.5
    epsilon = 1e-10
    
    bledy = []
    iteracje = 0
    max_iter = 50
    
    for i in range(max_iter):
        x_prev = x_current.copy()
        
        cel = lambda v: zewnetrzna_funkcja_kary(v, rho) if zewnetrzna else wewnetrzna_funkcja_kary(v, rho)
        options = {'maxiter': 10, 'disp': False}
        
        res = minimize(cel, x_current, method=metoda_podrzedna, options=options)
        x_current = res.x
        
        blad = np.linalg.norm(x_current - x_prev)
        bledy.append(blad)
        iteracje += 1
        
        if zewnetrzna:
            rho *= alpha_zewn
        else:
            rho *= alpha_wewn
            
        if blad <= epsilon and i > 1:
            break

    return x_current, f(x_current), bledy

# --- PARAMETRY I URUCHOMIENIE ---
x0 = [-2.5, 3.0]

print("--- METODA ZEWNĘTRZNEJ FUNKCJI KARY ---")
x_z_cg, f_z_cg, b_z_cg = optymalizuj(zewnetrzna_funkcja_kary, 'CG', x0, zewnetrzna=True)
x_z_nw, f_z_nw, b_z_nw = optymalizuj(zewnetrzna_funkcja_kary, 'BFGS', x0, zewnetrzna=True)
print(f"CG (Fletcher-Reeves): x = {x_z_cg}, f(x) = {f_z_cg:.6f}")
print(f"BFGS (Quasi-Newton):  x = {x_z_nw}, f(x) = {f_z_nw:.6f}\n")

print("--- METODA WEWNĘTRZNEJ FUNKCJI KARY ---")
x_w_cg, f_w_cg, b_w_cg = optymalizuj(wewnetrzna_funkcja_kary, 'CG', x0, zewnetrzna=False)
x_w_nw, f_w_nw, b_w_nw = optymalizuj(wewnetrzna_funkcja_kary, 'BFGS', x0, zewnetrzna=False)
print(f"CG (Fletcher-Reeves): x = {x_w_cg}, f(x) = {f_w_cg:.6f}")
print(f"BFGS (Quasi-Newton):  x = {x_w_nw}, f(x) = {f_w_nw:.6f}")

# --- WYKRES BŁĘDÓW (POPRAWIONO STRINGI 'r') ---
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(range(1, len(b_z_cg)+1), b_z_cg, label='Fletcher-Reeves (CG)', marker='o')
plt.plot(range(1, len(b_z_nw)+1), b_z_nw, label='Newton (BFGS)', marker='s')
plt.yscale('log')
plt.title(r'Zewnętrzna funkcja kary: $\epsilon(n)$')
plt.xlabel('Liczba iteracji nadrzędnych')
plt.ylabel('Błąd (skala logarytmiczna)')
plt.grid(True, which="both", ls="--")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(range(1, len(b_w_cg)+1), b_w_cg, label='Fletcher-Reeves (CG)', marker='o')
plt.plot(range(1, len(b_w_nw)+1), b_w_nw, label='Newton (BFGS)', marker='s')
plt.yscale('log')
plt.title(r'Wewnętrzna funkcja kary: $\epsilon(n)$')
plt.xlabel('Liczba iteracji nadrzędnych')
plt.ylabel('Błąd (skala logarytmiczna)')
plt.grid(True, which="both", ls="--")
plt.legend()

plt.tight_layout()
plt.show()
import numpy as np
import matplotlib.pyplot as plt

# 1. Zmiana globalnego stylu wykresu na bardziej profesjonalny
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    try:
        plt.style.use('seaborn-whitegrid')
    except:
        plt.style.use('ggplot')

# 2. Definicja funkcji, gradientu i hesjanu
def f(x):
    return (x[0] - 10)**2 + (x[0]*x[1] - 50000)**2

def grad_f(x):
    df_dx = 2*(x[0] - 10) + 2*(x[0]*x[1] - 50000)*x[1]
    df_dy = 2*(x[0]*x[1] - 50000)*x[0]
    return np.array([df_dx, df_dy])

def hessian_f(x):
    h11 = 2 + 2*x[1]**2
    h12 = 4*x[0]*x[1] - 100000
    h22 = 2*x[0]**2
    return np.array([[h11, h12], 
                     [h12, h22]])

# 3. Niedokładna minimalizacja kierunkowa - Reguła Goldsteina
def goldstein_search(x, d, m1=0.1, m2=0.9, max_ls_iter=100):
    tau = 1.0
    tau_min = 0.0
    tau_max = np.inf
    g0 = f(x)
    g_prime0 = np.dot(grad_f(x), d)
    
    if g_prime0 >= 0:
        return 1e-4

    for _ in range(max_ls_iter):
        x_new = x + tau * d
        g_tau = f(x_new)
        
        if g_tau > g0 + m1 * tau * g_prime0:
            tau_max = tau
            tau = (tau_min + tau_max) / 2.0
        elif g_tau < g0 + m2 * tau * g_prime0:
            tau_min = tau
            if np.isinf(tau_max):
                tau *= 2.0
            else:
                tau = (tau_min + tau_max) / 2.0
        else:
            break
            
    return tau

# 4. Główna pętla optymalizacyjna
def optimize(method, x0, epsilon, max_iter=500):
    x = np.array(x0, dtype=float)
    errors = []
    d_prev = None
    grad_prev = None
    
    for i in range(max_iter):
        grad = grad_f(x)
        err = np.linalg.norm(grad)
        errors.append(err)
        
        if err <= epsilon:
            break
            
        if method == 'najszybszy_spadek':
            d = -grad
            
        elif method == 'newton':
            H = hessian_f(x)
            try:
                d = np.linalg.solve(H, -grad)
            except np.linalg.LinAlgError:
                d = -grad
                
        elif method == 'cg_standard':
            if i == 0:
                d = -grad
            else:
                H = hessian_f(x)
                licznik = np.dot(grad, np.dot(H, d_prev))
                mianownik = np.dot(d_prev, np.dot(H, d_prev))
                gamma = licznik / (mianownik + 1e-12)
                d = -grad + gamma * d_prev
                
        elif method == 'cg_fr':
            if i == 0:
                d = -grad
            else:
                licznik = np.dot(grad, grad)
                mianownik = np.dot(grad_prev, grad_prev)
                gamma = licznik / (mianownik + 1e-12)
                d = -grad + gamma * d_prev
                
        elif method == 'cg_pr':
            if i == 0:
                d = -grad
            else:
                licznik = np.dot(grad - grad_prev, grad)
                mianownik = np.dot(grad_prev, grad_prev)
                gamma = licznik / (mianownik + 1e-12)
                d = -grad + gamma * d_prev

        if np.dot(grad, d) > 0:
            d = -grad

        tau = goldstein_search(x, d)
        
        d_prev = d
        grad_prev = grad
        x = x + tau * d
        
    return x, len(errors)-1, errors

# 5. Parametry wejściowe
punkty_startowe = [
    [0.0, 0.0],
    [10.0, 4900.0]  
]
epsilony_tabela = [10**-1, 10**-2, 10**-3]
epsilon_wykres = 10**-10

kolory_metod = {
    'najszybszy_spadek': 'tab:blue',
    'newton': 'tab:orange',
    'cg_standard': 'tab:green',
    'cg_fr': 'tab:red',
    'cg_pr': 'tab:purple'
}

# NOWY, CZYSTELNIEJSZY PODZIAŁ NA GRUPY
grupa_1 = {
    'najszybszy_spadek': 'Najszybszego Spadku',
    'newton': 'Newtona',
    'cg_standard': 'CG Standard'
}
grupa_2 = {
    'cg_fr': 'CG Fletchera-Reevesa',
    'cg_pr': 'CG Polaka-Ribiere\'a'
}
wszystkie_metody = {
    'najszybszy_spadek': 'Najszybszego Spadku',
    'newton': 'Newtona',
    'cg_standard': 'CG Standard',
    'cg_fr': 'CG Fletchera-Reevesa',
    'cg_pr': 'CG Polaka-Ribiere\'a'
}

# 6. Generowanie Tabel
print("===== GENEROWANIE TABEL Z WYNIKAMI =====")
for pt_idx, x0 in enumerate(punkty_startowe):
    print(f"\n---> Tabela dla punktu startowego nr {pt_idx+1}: x0 = {x0}")
    print(f"{'Metoda':<22} | {'Epsilon':<8} | {'Iteracje':<10} | {'x':<15} | {'y':<15} | {'f(x,y)'}")
    print("-" * 90)
    
    for met_klucz, met_nazwa in wszystkie_metody.items():
        for eps in epsilony_tabela:
            x_opt, iters, _ = optimize(met_klucz, x0, eps)
            wartosc_f = f(x_opt)
            print(f"{met_nazwa:<22} | {eps:<8} | {iters:<10} | {x_opt[0]:<15.6f} | {x_opt[1]:<15.6f} | {wartosc_f:.6e}")
        print("-" * 90)

# 7. Generowanie Wykresów
print("\n===== GENEROWANIE WYKRESÓW =====")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

for pt_idx, x0 in enumerate(punkty_startowe):
    
    # --- Wykres z lewej (Grupa 1: Stabilniejsze wizualnie) ---
    ax_g1 = axes[pt_idx, 0]
    ax_g1.set_title(f"Grupa 1: Najszybszy Spadek, Newton, CG Standard\nPunkt startowy: {x0}")
    ax_g1.set_xlabel("Liczba iteracji (n)")
    ax_g1.set_ylabel("Błąd $\\epsilon(n) = ||\\nabla f(x)||$")
    ax_g1.set_yscale("log")
    ax_g1.set_xlim(0, 500)

    for met_klucz, met_nazwa in grupa_1.items():
        _, _, errors = optimize(met_klucz, x0, epsilon_wykres)
        ax_g1.plot(range(len(errors)), errors, label=met_nazwa, linewidth=2, color=kolory_metod[met_klucz])
        
    ax_g1.legend()
    ax_g1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # --- Wykres z prawej (Grupa 2: Silnie oscylujące warianty) ---
    ax_g2 = axes[pt_idx, 1]
    ax_g2.set_title(f"Grupa 2: CG Fletchera-Reevesa, CG Polaka-Ribiere'a\nPunkt startowy: {x0}")
    ax_g2.set_xlabel("Liczba iteracji (n)")
    ax_g2.set_ylabel("Błąd $\\epsilon(n) = ||\\nabla f(x)||$")
    ax_g2.set_yscale("log")
    ax_g2.set_xlim(0, 500)

    for met_klucz, met_nazwa in grupa_2.items():
        _, _, errors = optimize(met_klucz, x0, epsilon_wykres)
        ax_g2.plot(range(len(errors)), errors, label=met_nazwa, linewidth=1.5, alpha=1.0, color=kolory_metod[met_klucz])
        
    ax_g2.legend()
    ax_g2.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

plt.tight_layout(pad=3.0)
plt.show()

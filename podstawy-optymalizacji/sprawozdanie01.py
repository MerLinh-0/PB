import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator


# Definicja funkcji oraz jej pochodnych
def f(x):
    return 6*x**4 + 40*x**3 + 69*x**2 - 18*x + 4

def df(x):
    return 24*x**3 + 120*x**2 + 138*x - 18

def ddf(x):
    return 72*x**2 + 240*x + 138

# Metoda ekspansji do poszukiwania przedziału izolacji ekstremum
def ekspansja(x0, d, is_max=False):
    # Jeśli szukamy maksimum, operujemy na -f(x)
    func = lambda x: -f(x) if is_max else f(x)
    
    x_prev = x0
    x_curr = x0 + d
    
    if func(x_curr) > func(x_prev):
        d = -d
        x_curr = x0 + d
        if func(x_curr) > func(x_prev):
            return [min(x0 - abs(d), x0 + abs(d)), max(x0 - abs(d), x0 + abs(d))]
            
    step = 1
    while True:
        x_next = x_curr + d * (2 ** step)
        if func(x_next) >= func(x_curr):
            # Zapewnienie, że szerokość przedziału >= 0.5
            a, b = min(x_prev, x_next), max(x_prev, x_next)
            if b - a < 0.5:
                center = (a + b) / 2
                a, b = center - 0.25, center + 0.25
            return [a, b]
        x_prev = x_curr
        x_curr = x_next
        step += 1

# Metoda stycznych (Newtona)
def newton_method(x0, eps_target=1e-10, max_iter=100):
    x = x0
    errors = []
    for i in range(max_iter):
        val_df = df(x)
        errors.append(abs(val_df))
        if abs(val_df) < eps_target and i > 0:
            break
        x = x - val_df / ddf(x)
    return x, f(x), i, errors

# Metoda siecznych
def secant_method(x0, x1, eps_target=1e-10, max_iter=100):
    errors = [abs(df(x0))]
    for i in range(1, max_iter):
        val_df0 = df(x0)
        val_df1 = df(x1)
        errors.append(abs(val_df1))
        
        if abs(val_df1) < eps_target:
            break
        if val_df1 - val_df0 == 0:
            break
            
        x_next = x1 - val_df1 * (x1 - x0) / (val_df1 - val_df0)
        x0, x1 = x1, x_next
    return x1, f(x1), i, errors

# Metoda interpolacji sześciennej Davidona
def davidon_method(x1, x2, eps_target=1e-10, max_iter=100, is_max=False):
    # Do iteracji używamy pochodnej
    errors = [abs(df(x1))]
    sign_f = -1 if is_max else 1
    
    for i in range(1, max_iter):
        f1, f2 = sign_f*f(x1), sign_f*f(x2)
        df1, df2 = sign_f*df(x1), sign_f*df(x2)
        errors.append(abs(df(x2)))
        
        if abs(df2) < eps_target:
            break
            
        z = 3 * (f1 - f2) / (x2 - x1) + df1 + df2
        w_term = z**2 - df1 * df2
        if w_term < 0:
            break # Zabezpieczenie przed wartością zespoloną
        w = np.sqrt(w_term)
        
        if x1 > x2:
            w = -w
            
        # Zabezpieczenie mianownika
        denom = df2 - df1 + 2 * w
        if denom == 0:
            break
            
        r = (df2 + w - z) / denom
        x_next = x2 - r * (x2 - x1)
        
        x1, x2 = x2, x_next
    return x2, f(x2), i, errors

# Parametry początkowe dla trzech ekstremów
extrema_setup = [
    {"name": "Pierwsze ekstremum (Minimum)", "x0": -4.0, "d": 0.1, "is_max": False, "x1_sec": -2.5, "x2_sec": -2.7},
    {"name": "Drugie ekstremum (Maksimum)", "x0": -1.5, "d": -0.1, "is_max": True, "x1_sec": -1.5, "x2_sec": -1.8},
    {"name": "Trzecie ekstremum (Minimum)", "x0": 1.0, "d": -0.1, "is_max": False, "x1_sec": 1.0, "x2_sec": 0.8}
]

epsilons = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]

for idx, setup in enumerate(extrema_setup):
    print(f"\n{'='*50}\n{setup['name']}")
    
    # Ekspansja
    interval = ekspansja(setup["x0"], setup["d"], is_max=setup["is_max"])
    print(f"Przedział lokalizacji: [{interval[0]:.4f}, {interval[1]:.4f}] (szerokość: {interval[1]-interval[0]:.4f})")
    
    # Punkty startowe (dobrane z przedziału)
    start_newton = (interval[0] + interval[1]) / 2
    
    # Rozwiązania dla epsilon = 10^-10 do wykresów
    res_newton = newton_method(start_newton)
    res_secant = secant_method(setup["x1_sec"], setup["x2_sec"])
    res_davidon = davidon_method(setup["x1_sec"], setup["x2_sec"], is_max=setup["is_max"])
    
    # Zbieranie danych do tabeli (dla zadanych epsilonów)
    table_data = []
    for eps in epsilons:
        _, _, iter_n, _ = newton_method(start_newton, eps_target=eps)
        _, _, iter_s, _ = secant_method(setup["x1_sec"], setup["x2_sec"], eps_target=eps)
        _, _, iter_d, _ = davidon_method(setup["x1_sec"], setup["x2_sec"], eps_target=eps, is_max=setup["is_max"])
        
        table_data.append([
            f"10^{int(np.log10(eps))}", 
            iter_d, f"{res_davidon[0]:.6f}", f"{res_davidon[1]:.6f}",
            iter_s, f"{res_secant[0]:.6f}", f"{res_secant[1]:.6f}",
            iter_n, f"{res_newton[0]:.6f}", f"{res_newton[1]:.6f}"
        ])
        
    df_table = pd.DataFrame(table_data, columns=[
        "Epsilon", "Davidon (Iter)", "Davidon X", "Davidon f(x)", 
        "Sieczne (Iter)", "Sieczne X", "Sieczne f(x)",
        "Styczne (Iter)", "Styczne X", "Styczne f(x)"
    ])
    
    print("\nTabela wyników:")
    print(df_table.to_string(index=False))

    # Wykres błędu w skali logarytmicznej
    plt.figure(figsize=(10, 6))
    
    # Przygotowanie danych do rysowania (pomijanie zer, aby log zadziałał)
    plot_err_d = [max(e, 1e-16) for e in res_davidon[3]]
    plot_err_s = [max(e, 1e-16) for e in res_secant[3]]
    plot_err_n = [max(e, 1e-16) for e in res_newton[3]]

    plt.plot(range(len(plot_err_d)), plot_err_d, marker='o', label='Metoda Davidona')
    plt.plot(range(len(plot_err_s)), plot_err_s, marker='s', label='Metoda siecznych')
    plt.plot(range(len(plot_err_n)), plot_err_n, marker='^', label='Metoda stycznych (Newtona)')

    plt.yscale('log')
    plt.xlabel('Liczba iteracji (n)')
    plt.ylabel(r'Błąd $\epsilon$ (wartość bezwzględna pochodnej)')
    plt.title(f'Wykres funkcji błędu od liczby iteracji - {setup["name"]}')
    
    # Wymuszenie całkowitych etykiet na osi X
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.axhline(y=1e-10, color='r', linestyle='--', alpha=0.5, label=r'$\epsilon = 10^{-10}$')
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    
    # ROZWIĄZANIE BŁĘDU: Zapis do pliku zamiast plt.show()
    nazwa_pliku = f"wykres_ekstremum_{idx+1}.png"
    plt.savefig(nazwa_pliku, dpi=300, bbox_inches='tight')
    print(f"\n---> Zapisano wykres do pliku: {nazwa_pliku}\n")
    
    # Zamknięcie figury, aby nie nakładały się na siebie w pamięci
    plt.close()
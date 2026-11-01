import numpy as np
import matplotlib.pyplot as plt

# Zdefiniowanie badanej funkcji oraz jej pochodnych
def f(x):
    return 6*x**4 + 40*x**3 + 69*x**2 - 18*x + 4

def df(x):
    return 24*x**3 + 120*x**2 + 138*x - 18

def ddf(x):
    return 72*x**2 + 240*x + 138

# Funkcje pomocnicze dla szukania maksimum (g = -f)
def g(x):
    return -f(x)

def dg(x):
    return -df(x)

def ddg(x):
    return -ddf(x)

def format_val(val):
    """Zwraca wartość zaokrągloną do 5 miejsc po przecinku"""
    return f"{val:.5f}" if val is not None else "---"

def expansion_method(func, x0, dx):
    """
    Zmodyfikowana metoda ekspansji Boxa-Daviesa-Swanna.
    Zwraca przedział [a, b], w którym znajduje się minimum funkcji func.
    """
    x = [x0]
    # Sprawdzamy krok w prawo
    x1 = x0 + dx
    if func(x1) >= func(x0):
        # Funkcja rośnie w prawo, więc szukamy w lewo
        b = x1
        i = 0
        while True:
            x_minus = x0 - (2**i)*dx
            x.append(x_minus)
            if func(x_minus) >= func(x[-2]):
                a = x_minus
                break
            i += 1
        return min(a, b), max(a, b)
    else:
        # Funkcja maleje w prawo, szukamy w prawo
        a = x0 - dx # Zabezpieczenie przedziału z lewej
        i = 1
        x.append(x1)
        while True:
            x_plus = x[-1] + (2**i)*dx
            x.append(x_plus)
            if func(x_plus) >= func(x[-2]):
                b = x_plus
                a = x[-3] if len(x) >= 3 else a
                break
            i += 1
        return min(a, b), max(a, b)

def method_davidon(func, dfunc, a, b, eps_target=1e-10, max_iter=100):
    """Metoda interpolacji sześciennej Davidona."""
    history = []
    a_curr, b_curr = a, b
    
    for k in range(1, max_iter + 1):
        # Układ równań do interpolacji Hermite'a
        M = np.array([
            [a_curr**3, a_curr**2, a_curr, 1],
            [3*a_curr**2, 2*a_curr, 1, 0],
            [b_curr**3, b_curr**2, b_curr, 1],
            [3*b_curr**2, 2*b_curr, 1, 0]
        ])
        V = np.array([func(a_curr), dfunc(a_curr), func(b_curr), dfunc(b_curr)])
        
        try:
            coeffs = np.linalg.solve(M, V)
        except np.linalg.LinAlgError:
            break # Macierz osobliwa
            
        A, B, C_coeff, D = coeffs
        
        # Wyznaczanie minimum wielomianu
        discriminant = B**2 - 3*A*C_coeff
        if discriminant < 0 or A == 0:
            break
            
        x_min = (-B + np.sqrt(discriminant)) / (3*A)
        err = abs(dfunc(x_min))
        history.append((k, x_min, func(x_min), err))
        
        if err <= eps_target:
            break
            
        # Aktualizacja przedziału
        if dfunc(x_min) < 0:
            a_curr = x_min
        else:
            b_curr = x_min
            
    return history

def method_secant(func, dfunc, a, b, eps_target=1e-10, max_iter=100):
    """Metoda siecznych."""
    history = []
    a_curr, b_curr = a, b
    
    for k in range(1, max_iter + 1):
        df_a = dfunc(a_curr)
        df_b = dfunc(b_curr)
        
        if df_b - df_a == 0:
            break
            
        x_min = a_curr - df_a * ((b_curr - a_curr) / (df_b - df_a))
        err = abs(dfunc(x_min))
        history.append((k, x_min, func(x_min), err))
        
        if err <= eps_target:
            break
            
        if dfunc(x_min) < 0:
            a_curr = x_min
        else:
            b_curr = x_min
            
    return history

def method_newton(func, dfunc, ddfunc, x0, eps_target=1e-10, max_iter=100):
    """Metoda stycznych (Newtona)."""
    history = []
    x_curr = x0
    
    for k in range(1, max_iter + 1):
        ddf_val = ddfunc(x_curr)
        if ddf_val == 0:
            break
            
        x_new = x_curr - dfunc(x_curr) / ddf_val
        err = abs(dfunc(x_new))
        history.append((k, x_new, func(x_new), err))
        
        if err <= eps_target:
            break
        x_curr = x_new
        
    return history

def extract_for_eps(history, eps):
    """Zwraca (iteracja, x, f(x)) dla pierwszego wystąpienia błędu <= eps"""
    for it, x_val, f_val, err in history:
        if err <= eps:
            return it, x_val, f_val
    # Jeśli nie osiągnięto dokładności, zwróć ostatni
    if history:
        return history[-1][0], history[-1][1], history[-1][2]
    return None, None, None

def print_table(extr_num, kind, x0, dx, func_used, dfunc_used, ddfunc_used, is_max):
    print(f"\n==========================================================")
    print(f"Rodzaj {extr_num} ekstremum: {'Maksimum' if is_max else 'Minimum'}")
    
    a, b = expansion_method(func_used, x0, dx)
    # Zapewnienie szerokości przedziału >= 0.5
    while b - a < 0.5:
        a -= 0.1
        b += 0.1

    print(f"Parametry metody ekspansji: x0 = {x0}, delta_x = {dx}")
    print(f"Przedział lokalizacji: [{format_val(a)}; {format_val(b)}]")
    print(f"----------------------------------------------------------")
    print(f"Tabela dla {extr_num} ekstremum:")
    print(f"eps    | Metoda Davidona               | Metoda siecznych              | Metoda stycznych (Newtona)")
    print(f"       | Iter | X        | f(X)      | Iter | X        | f(X)      | Iter | X        | f(X)")
    print(f"--------------------------------------------------------------------------------------------------")
    
    # Dla Newtona bierzemy optymalny koniec przedziału jako punkt startowy
    x0_newton = b if ddfunc_used(b) > 0 else a
    
    hist_dav = method_davidon(func_used, dfunc_used, a, b)
    hist_sec = method_secant(func_used, dfunc_used, a, b)
    hist_new = method_newton(func_used, dfunc_used, ddfunc_used, x0_newton)
    
    epsilons = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]
    eps_labels = ["10^-1", "10^-2", "10^-3", "10^-4", "10^-5"]
    
    for eps, label in zip(epsilons, eps_labels):
        it_d, x_d, f_d = extract_for_eps(hist_dav, eps)
        it_s, x_s, f_s = extract_for_eps(hist_sec, eps)
        it_n, x_n, f_n = extract_for_eps(hist_new, eps)
        
        # Odtworzenie oryginalnej wartosci f(x) w przypadku szukania maksimum
        if is_max:
            f_d = -f_d if f_d is not None else None
            f_s = -f_s if f_s is not None else None
            f_n = -f_n if f_n is not None else None

        row = f"{label:<6} | "
        row += f"{it_d:<4} | {format_val(x_d):<8} | {format_val(f_d):<9} | "
        row += f"{it_s:<4} | {format_val(x_s):<8} | {format_val(f_s):<9} | "
        row += f"{it_n:<4} | {format_val(x_n):<8} | {format_val(f_n):<9}"
        print(row)
        
    return hist_dav, hist_sec, hist_new

def plot_errors(extr_num, hist_dav, hist_sec, hist_new):
    plt.figure(figsize=(10, 6))
    
    dav_x = [h[0] for h in hist_dav]
    dav_y = [h[3] for h in hist_dav]
    plt.plot(dav_x, dav_y, label='Metoda Davidona', marker='o')
    
    sec_x = [h[0] for h in hist_sec]
    sec_y = [h[3] for h in hist_sec]
    plt.plot(sec_x, sec_y, label='Metoda siecznych', marker='s')
    
    new_x = [h[0] for h in hist_new]
    new_y = [h[3] for h in hist_new]
    plt.plot(new_x, new_y, label='Metoda Newtona', marker='^')
    
    plt.yscale('log')
    plt.xlabel('Liczba iteracji (n)')
    plt.ylabel('Błąd (eps)')
    plt.title(f'Wykres funkcji błędu eps(n) - {extr_num} ekstremum')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    
    # Wymuszenie całkowitych etykiet osi X
    ax = plt.gca()
    ax.xaxis.get_major_locator().set_params(integer=True)
    
    plt.show()

# Konfiguracja dla 3 ekstremów
# Z wykresu pochodnej widzimy ekstrema w okolicach: -3.6 (Min), -1.5 (Max), 0.1 (Min)

hist_d1, hist_s1, hist_n1 = print_table("pierwszego", f, -4.0, 0.1, f, df, ddf, is_max=False)
plot_errors("pierwsze", hist_d1, hist_s1, hist_n1)

hist_d2, hist_s2, hist_n2 = print_table("drugiego", g, -2.0, 0.1, g, dg, ddg, is_max=True)
plot_errors("drugie", hist_d2, hist_s2, hist_n2)

hist_d3, hist_s3, hist_n3 = print_table("trzeciego", f, 0.5, 0.2, f, df, ddf, is_max=False)
plot_errors("trzecie", hist_d3, hist_s3, hist_n3)
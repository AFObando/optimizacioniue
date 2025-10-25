import numpy as np


# MÉTODO DE SECCIÓN ÁUREA
def seccion_aurea(f, a, b, tol):
    phi = (1 + np.sqrt(5)) / 2
    resphi = 2 - phi
    iteraciones = []
    k = 1
    while abs(b - a) > tol:
        c = a + resphi * (b - a)
        d = b - resphi * (b - a)
        fc, fd = f(c), f(d)
        iteraciones.append({
            "Iteración": k,
            "a": a, "b": b,
            "x1": c, "x2": d,
            "f(x1)": fc, "f(x2)": fd
        })
        if fc < fd:
            b = d
        else:
            a = c
        k += 1
    return (b + a) / 2, iteraciones



# MÉTODO DE FIBONACCI
def fibonacci(f, a, b, n):

    fib = [1, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])

  

    iteraciones = []

    x1 = a + (fib[n - 3] / fib[n - 1]) * (b - a)
    x2 = a + (fib[n - 2] / fib[n - 1]) * (b - a)
    f1, f2 = f(x1), f(x2)

    for k in range(1, n - 2):
        iteraciones.append({
            "Iteración": k,
            "a": a, "b": b,
            "x1": x1, "x2": x2,
            "f(x1)": f1, "f(x2)": f2
        })

        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + (fib[n - k - 2] / fib[n - k - 1]) * (b - a)
            f2 = f(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (fib[n - k - 3] / fib[n - k - 1]) * (b - a)
            f1 = f(x1)

    x_min = (a + b) / 2
    return x_min, iteraciones



# BÚSQUEDA SECUENCIAL
def busqueda_secuencial(f, a, b, step):
    x = a
    best_x = x
    best_val = f(x)
    iteraciones = []
    k = 1
    while x <= b:
        val = f(x)
        iteraciones.append({"Iteración": k, "x": x, "f(x)": val})
        if val < best_val:
            best_val = val
            best_x = x
        x += step
        k += 1
    return best_x, iteraciones


# BÚSQUEDA DICOTÓMICA
def busqueda_dicotomica(f, a, b, tol, max_iter):
    delta = tol / 4
    iteraciones = []
    k = 1
    while abs(b - a) > tol and k <= max_iter:
        mid = (a + b) / 2
        x1 = mid - delta
        x2 = mid + delta
        fx1, fx2 = f(x1), f(x2)
        iteraciones.append({
            "Iteración": k, "a": a, "b": b, "x1": x1, "x2": x2,
            "f(x1)": fx1, "f(x2)": fx2
        })
        if fx1 < fx2:
            b = x2
        else:
            a = x1
        k += 1
    res = (a + b) / 2
    return res, iteraciones


# BISECCIÓN 
def biseccion(f_prime, a, b, tol):
    iteraciones = []
    k = 1
    while (b - a) / 2 > tol:
        mid = (a + b) / 2
        f_a, f_mid = f_prime(a), f_prime(mid)
        iteraciones.append({
            "Iteración": k, "a": a, "b": b, "mid": mid,
            "f'(a)": f_a, "f'(mid)": f_mid
        })
        if f_mid == 0:
            return mid, iteraciones
        elif f_a * f_mid < 0:
            b = mid
        else:
            a = mid
        k += 1
    return (a + b) / 2, iteraciones



# NEWTON UNIDIMENSIONAL
def newton_unidimensional(f_prime, f_double_prime, x0, tol, max_iter):
    iteraciones = []
    x = x0
    for k in range(max_iter):
        fp = f_prime(x)
        fpp = f_double_prime(x)
        iteraciones.append({
            "Iteración": k+1, "x": x, "f'(x)": fp, "f''(x)": fpp
        })
        if abs(fpp) < 1e-10: 
            break
        x_new = x - fp / fpp
        if abs(x_new-x) < tol:
            return x_new, iteraciones
        x = x_new
    return x, iteraciones

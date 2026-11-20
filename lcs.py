"""LCS (subsecuencia comun mas larga) de tres formas. Ejecutar: python lcs.py"""
import csv
import random
import time
import tracemalloc


def lcs_recursiva(x, y):
    """A: recursion directa, sin memorizar. Tiempo O(2^(m+n))."""
    if not x or not y:
        return ""
    if x[0] == y[0]:
        return x[0] + lcs_recursiva(x[1:], y[1:])
    a, b = lcs_recursiva(x[1:], y), lcs_recursiva(x, y[1:])
    return a if len(a) >= len(b) else b


def ultima_fila(x, y):
    """Longitudes LCS de x contra cada prefijo de y, usando solo una fila."""
    fila = [0] * (len(y) + 1)
    for c in x:
        anterior = 0
        for j in range(1, len(y) + 1):
            guardado = fila[j]
            fila[j] = anterior + 1 if c == y[j - 1] else max(fila[j], fila[j - 1])
            anterior = guardado
    return fila


def lcs_hirschberg(x, y):
    """B: divide y venceras. Tiempo O(mn), memoria O(n)."""
    if not x or not y:
        return ""
    if len(x) == 1:
        return x if x in y else ""
    mitad = len(x) // 2
    f1 = ultima_fila(x[:mitad], y)
    f2 = ultima_fila(x[mitad:][::-1], y[::-1])
    n = len(y)
    k = max(range(n + 1), key=lambda j: f1[j] + f2[n - j])
    return lcs_hirschberg(x[:mitad], y[:k]) + lcs_hirschberg(x[mitad:], y[k:])


def lcs_tabla(x, y):
    """C: programacion dinamica con tabla. Tiempo y memoria O(mn)."""
    m, n = len(x), len(y)
    t = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            t[i][j] = t[i + 1][j + 1] + 1 if x[i] == y[j] else max(t[i + 1][j], t[i][j + 1])
    res, i, j = [], 0, 0
    while i < m and j < n:
        if x[i] == y[j]:
            res.append(x[i]); i += 1; j += 1
        elif t[i + 1][j] >= t[i][j + 1]:
            i += 1
        else:
            j += 1
    return "".join(res)


def es_subsecuencia(s, t):
    it = iter(t)
    return all(c in it for c in s)


def medir(f, x, y):
    """Devuelve (longitud LCS, mediana de 3 tiempos de CPU en s, memoria pico en KB)."""
    tiempos = []
    for _ in range(3):
        t0 = time.process_time()
        s = f(x, y)
        tiempos.append(time.process_time() - t0)
    assert es_subsecuencia(s, x) and es_subsecuencia(s, y)
    cpu = sorted(tiempos)[1]
    tracemalloc.start()
    f(x, y)
    pico = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return len(s), cpu, pico / 1024


def cadenas(n):
    r = random.Random(n)
    return ["".join(r.choice("ACGT") for _ in range(n)) for _ in range(2)]


if __name__ == "__main__":
    filas = [["Algoritmo", "n", "LCS", "CPU (s)", "Memoria pico (KB)"]]
    pruebas = [("A recursiva", lcs_recursiva, [8, 10, 12, 14, 16]),
               ("B Hirschberg", lcs_hirschberg, [100, 250, 500, 1000, 2000]),
               ("C tabla", lcs_tabla, [100, 250, 500, 1000, 2000])]
    for nombre, f, tamanos in pruebas:
        for n in tamanos:
            largo, cpu, mem = medir(f, *cadenas(n))
            fila = [nombre, n, largo, f"{cpu:.3f}", f"{mem:.0f}"]
            filas.append(fila)
            print(f"{nombre:<14} | n={n:<4} | LCS={largo:<4} | CPU={cpu:.3f}s | Mem={mem:.0f} KB", flush=True)
    with open("resultados.csv", "w", newline="", encoding="utf-8") as f_csv:
        csv.writer(f_csv).writerows(filas)

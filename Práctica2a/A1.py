import math

def dpois1(k: int, lam: float) -> float:
    """
    Devuelve la probabilidad P(X = k) para X ~ Poisson(λ)
    """
    if k < 0:
        return 0.0
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def ppois1(k: int, lam: float) -> float:
    """
    Devuelve la probabilidad acumulada P(X ≤ k)
    """
    if k < 0:
        return 0.0
    total = 0.0
    for i in range(0, k + 1):
        total += dpois1(i, lam)
    return total


def qpois1(q: float, lam: float) -> int:
    """
    Devuelve el menor valor de k tal que P(X ≤ k) ≥ q
    """
    if not 0 <= q <= 1:
        raise ValueError("q debe estar entre 0 y 1")

    k = 0
    acumulado = dpois1(k, lam)
    while acumulado < q:
        k += 1
        acumulado += dpois1(k, lam)
    return k


# --- Ejemplo de uso ---
if __name__ == "__main__":
    lam = 3.5
    print("dpois1(2, 3.5) =", dpois1(2, lam))
    print("ppois1(2, 3.5) =", ppois1(2, lam))
    print("qpois1(0.8, 3.5) =", qpois1(0.8, lam))

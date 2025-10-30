from scipy.stats import poisson

def dpois2(k, lam) -> float:
    return float(poisson.pmf(k, mu=lam))

def ppois2(k, lam) -> float:
    return float(poisson.cdf(k, mu=lam))

def qpois2(q, lam) -> int:
    return int(poisson.ppf(q, mu=lam))

# --- Ejemplo de uso ---
if __name__ == "__main__":
    lam = 3.5
    print("dpois2(2, 3.5) =", dpois2(2, lam))
    print("ppois2(2, 3.5) =", ppois2(2, lam))
    print("qpois2(0.8, 3.5) =", qpois2(0.8, lam))

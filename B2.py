from scipy.stats import expon, weibull_min

# --- Distribución Exponencial ---

# Función de densidad f(t)
def dexp2(t, beta) -> float:
    """Densidad de probabilidad de la distribución exponencial."""
    return expon(scale=beta).pdf(t)

# Función de distribución F(t)
def pexp2(t, beta) -> float:
    """Función de distribución acumulada de la distribución exponencial."""
    return expon(scale=beta).cdf(t)

# Función de fiabilidad R(t)
def rexp2(t, beta) -> float:
    """Función de fiabilidad (supervivencia)."""
    return expon(scale=beta).sf(t)  # sf = survival function = 1 - cdf

# Función de riesgo h(t)
def hexp2(t, beta) -> float:
    """Función de riesgo (hazard function)."""
    f = dexp2(t, beta)
    R = rexp2(t, beta)
    return f / R

# Tiempo medio hasta el fallo E[T]
def mttf_exp2(beta) -> float:
    """Tiempo medio hasta el fallo (MTTF) para la exponencial."""
    return expon(scale=beta).mean()

# --- Distribución Weibull ---

# Función de densidad f(t)
def dweibull2(t, alpha, beta) -> float:
    """Densidad de probabilidad de la distribución Weibull."""
    return weibull_min(c=beta, scale=alpha).pdf(t)

# Función de distribución F(t)
def pweibull2(t, alpha, beta) -> float:
    """Función de distribución acumulada de la distribución Weibull."""
    return weibull_min(c=beta, scale=alpha).cdf(t)

# Función de fiabilidad R(t)
def rweibull2(t, alpha, beta) -> float:
    """Función de fiabilidad (supervivencia)."""
    return weibull_min(c=beta, scale=alpha).sf(t)

# Función de riesgo h(t)
def hweibull2(t, alpha, beta) -> float:
    """Función de riesgo (hazard function)."""
    f = dweibull2(t, alpha, beta)
    R = rweibull2(t, alpha, beta)
    return f / R

# Tiempo medio hasta el fallo E[T]
def mttf_weibull2(alpha, beta) -> float:
    """Tiempo medio hasta el fallo (MTTF) para la Weibull."""
    return weibull_min(c=beta, scale=alpha).mean()






if __name__ == "__main__":
    t = 5  # tiempo de ejemplo

    print("=== Distribución Exponencial ===")
    beta_exp = 3  # parámetro de escala (1/lambda)

    print(f"f({t}) = {dexp2(t, beta_exp):.5f}")  # Densidad
    print(f"F({t}) = {pexp2(t, beta_exp):.5f}")  # Distribución acumulada
    print(f"R({t}) = {rexp2(t, beta_exp):.5f}")  # Fiabilidad
    print(f"h({t}) = {hexp2(t, beta_exp):.5f}")  # Riesgo
    print(f"MTTF = {mttf_exp2(beta_exp):.5f}")   # Tiempo medio hasta el fallo

    print("\n=== Distribución Weibull ===")
    alpha_weib = 1000  # escala
    beta_weib = 1.5    # forma

    print(f"f({t}) = {dweibull2(t, alpha_weib, beta_weib):.8f}")  # Densidad
    print(f"F({t}) = {pweibull2(t, alpha_weib, beta_weib):.8f}")  # Distribución acumulada
    print(f"R({t}) = {rweibull2(t, alpha_weib, beta_weib):.8f}")  # Fiabilidad
    print(f"h({t}) = {hweibull2(t, alpha_weib, beta_weib):.8f}")  # Riesgo
    print(f"MTTF = {mttf_weibull2(alpha_weib, beta_weib):.5f}")   # Tiempo medio hasta el fallo
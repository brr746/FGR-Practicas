from math import exp, gamma

# --- Distribución Exponencial (parámetro de escala β) ---
# f(t): función de densidad
#   f(t) = (1/β) * e^(-t/β),  t >= 0
#        = 0                ,  t < 0
def dexp1(t, beta) -> float:
    if t < 0:
        return 0.0
    return (1.0 / beta) * exp(-t / beta)


# F(t): función de distribución acumulada
#   F(t) = 0                    , t < 0
#        = 1 - e^(-t/β)         , t >= 0
def pexp1(t, beta) -> float:
    if t < 0:
        return 0.0
    return 1.0 - exp(-t / beta)


# R(t): función de fiabilidad
#   R(t) = P(T >= t) = 1 - F(t)
#        = 1                , t < 0
#        = e^(-t/β)         , t >= 0
def rexp1(t, beta) -> float:
    if t < 0:
        return 1.0
    return exp(-t / beta)


# h(t): función de riesgo
#   h(t) = f(t) / R(t)
#        = (1/β) constante para t >= 0
def hexp1(t, beta) -> float:
    if t < 0:
        return 0.0
    # Para la exponencial, el riesgo es constante: 1/β
    return 1.0 / beta


# Tiempo medio hasta el fallo E[T] = MTTF
#   Para T ~ Exp(β):  E[T] = β
def mttf_exp1(beta) -> float:
    return beta



# --- Distribución Weibull T ~ W(α, β) ---
# f(t): función de densidad
#   f(t) = (α/β) * (t/β)^(α-1) * e^{-(t/β)^α},  t >= 0
#        = 0                                   ,  t < 0
def dweibull1(t, alpha, beta) -> float:
    if t < 0:
        return 0.0
    # (t/beta)**alpha aparece tanto en f como en F/R
    z = (t / beta) ** alpha
    return (alpha / beta) * (t / beta) ** (alpha - 1.0) * exp(-z)


# F(t): función de distribución acumulada
#   F(t) = 0                          , t < 0
#        = 1 - e^{-(t/β)^α}           , t >= 0
def pweibull1(t, alpha, beta) -> float:
    if t < 0:
        return 0.0
    z = (t / beta) ** alpha
    return 1.0 - exp(-z)


# R(t): función de fiabilidad
#   R(t) = 1 - F(t)
#        = 1                    , t < 0
#        = e^{-(t/β)^α}         , t >= 0
def rweibull1(t, alpha, beta) -> float:
    if t < 0:
        return 1.0
    z = (t / beta) ** alpha
    return exp(-z)


# h(t): función de riesgo
#   h(t) = f(t) / R(t)
#        = (α/β) * (t/β)^(α-1),  t >= 0
#        = 0                    , t < 0
def hweibull1(t, alpha, beta) -> float:
    if t < 0:
        return 0.0
    # Como R(t) = e^{-(t/β)^α}, al dividir f(t)/R(t) se simplifica la exponencial
    return (alpha / beta) * (t / beta) ** (alpha - 1.0)


# Tiempo medio hasta el fallo E[T] = MTTF
#   Para T ~ W(α, β):  E[T] = β * Γ(1 + 1/α)
def mttf_weibull1(alpha, beta) -> float:
    return beta * gamma(1.0 + 1.0 / alpha)

if __name__ == "__main__":
    t = 5  # tiempo de ejemplo

    print("=== Distribución Exponencial ===")
    beta_exp = 3  # parámetro de escala (1/lambda)

    print(f"f({t}) = {dexp1(t, beta_exp):.5f}")   # Densidad
    print(f"F({t}) = {pexp1(t, beta_exp):.5f}")   # Distribución acumulada
    print(f"R({t}) = {rexp1(t, beta_exp):.5f}")   # Fiabilidad
    print(f"h({t}) = {hexp1(t, beta_exp):.5f}")   # Riesgo
    print(f"MTTF = {mttf_exp1(beta_exp):.5f}")    # Tiempo medio hasta el fallo

    print("\n=== Distribución Weibull ===")
    alpha_weib = 1000  # escala (como en tu ejemplo original)
    beta_weib = 1.5    # forma  (como en tu ejemplo original)

    # Tus funciones usan: primero forma (α), luego escala (β).
    # Por eso pasamos beta_weib como α y alpha_weib como β.
    print(f"f({t}) = {dweibull1(t, beta_weib, alpha_weib):.8f}")   # Densidad
    print(f"F({t}) = {pweibull1(t, beta_weib, alpha_weib):.8f}")   # Distribución acumulada
    print(f"R({t}) = {rweibull1(t, beta_weib, alpha_weib):.8f}")   # Fiabilidad
    print(f"h({t}) = {hweibull1(t, beta_weib, alpha_weib):.8f}")   # Riesgo
    print(f"MTTF = {mttf_weibull1(beta_weib, alpha_weib):.5f}")    # Tiempo medio hasta el fallo

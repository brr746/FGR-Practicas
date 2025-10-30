# Si tu archivo se llama Practica3.py:
from EjercicioA3 import calcular_fiabilidad, simple, serie, paralelo
# Si se llama EjercicioA3.py, usa:
# from EjercicioA3 import calcular_fiabilidad, simple, serie, paralelo


def ejemplo_enunciado() -> float:
    # Componentes simples
    C1 = simple(0.8)
    C2 = simple(0.9)
    C3 = simple(0.75)
    C4 = simple(0.95)
    # Subsistemas
    S23 = serie(C2, C3)
    S123 = paralelo(C1, S23)
    # Sistema global
    S = serie(S123, C4)
    return calcular_fiabilidad(S)


if __name__ == "__main__":
    R = ejemplo_enunciado()
    print(f"Fiabilidad total (esperado 0.88825): {R:.5f}")

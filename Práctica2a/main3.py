# Si tu archivo se llama Practica3.py:
from Práctica2a.EjercicioA3 import calcular_fiabilidad, simple, serie, paralelo
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



def escenario_servidor() -> float:
    """
    Servidor en serie: [tarjeta_red] · [almacenamiento (3 discos en paralelo)] · [procesador (2 CPUs en paralelo)]
    Datos (fin de semana):
      - Red: R = 0.99
      - Cada disco: falla 0.2 -> R = 0.8 (3 en paralelo)
      - Cada CPU:  falla 0.25 -> R = 0.75 (2 en paralelo)
    """
    net = simple(0.99)

    # Almacenamiento: 3 discos redundantes (paralelo), cada uno R=0.8
    d1 = simple(0.8)
    d2 = simple(0.8)
    d3 = simple(0.8)
    storage = paralelo(d1, d2, d3)

    # Procesador: 2 CPUs redundantes (paralelo), cada una R=0.75
    c1 = simple(0.75)
    c2 = simple(0.75)
    cpu = paralelo(c1, c2)

    # Sistema global en serie
    sistema = serie(net, storage, cpu)
    return calcular_fiabilidad(sistema)


if __name__ == "__main__":
    R = escenario_servidor()
    print(f"Fiabilidad total (esperado 0.9207): {R:.6f}")
    # Verificación rápida (fallará si algo no cuadra)
    assert abs(R - 0.9207) < 1e-12
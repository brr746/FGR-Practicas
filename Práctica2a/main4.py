# Si tu archivo se llama Practica3.py:
from Práctica2a.EjercicioA3 import calcular_fiabilidad, simple, serie, paralelo
# Si se llama EjercicioA3.py, usa:
# from EjercicioA3 import calcular_fiabilidad, simple, serie, paralelo


def ejemplo_enunciado() -> float:
    # Componentes del servidor
    tarjeta_red = simple(0.99)

    # 3 discos duros en paralelo (cada uno R=0.8)
    disco1 = simple(0.8)
    disco2 = simple(0.8)
    disco3 = simple(0.8)
    almacenamiento = paralelo(disco1, disco2, disco3)

    # 2 procesadores en paralelo (cada uno R=0.75)
    proc1 = simple(0.75)
    proc2 = simple(0.75)
    procesadores = paralelo(proc1, proc2)

    # Sistema completo en serie
    servidor = serie(tarjeta_red, almacenamiento, procesadores)

    # Calcular fiabilidad
    return calcular_fiabilidad(servidor)

if __name__ == "__main__":
    R_servidor = ejemplo_enunciado()
    print(f"Fiabilidad del servidor: {R_servidor:.6f}")
    print(f"Probabilidad de fallo: {1 - R_servidor:.6f}")
    print(f"Disponibilidad: {R_servidor * 100:.2f}%")
    # Verificación numérica
    expected = 0.9207
    from math import isclose
    assert isclose(R_servidor, expected, rel_tol=1e-12, abs_tol=1e-12)
# main5.py — Ejercicio A5 (DBFs)
from math import isclose
from EjercicioA3 import calcular_fiabilidad, simple, serie, paralelo


def escenario_servidor_critico() -> float:
    """
    Subsistemas:
      - Firewall de borde (simple): R = 0.97
      - Alimentación (2 PSUs redundantes en paralelo): cada PSU falla 0.10 -> R_psu = 0.90
      - Refrigeración (3 ventiladores redundantes en paralelo): cada fan falla 0.05 -> R_fan = 0.95
    Sistema total = serie(firewall, alimentacion, refrigeracion)
    """
    # Firewall
    fw = simple(0.97)

    # Alimentación: 2 PSUs en paralelo (cada una R=0.90)
    psu1 = simple(0.90)
    psu2 = simple(0.90)
    alimentacion = paralelo(psu1, psu2)

    # Refrigeración: 3 ventiladores en paralelo (cada uno R=0.95)
    fan1 = simple(0.95)
    fan2 = simple(0.95)
    fan3 = simple(0.95)
    refrigeracion = paralelo(fan1, fan2, fan3)

    # Sistema global en serie
    sistema = serie(fw, alimentacion, refrigeracion)
    return calcular_fiabilidad(sistema)


def calculo_manual() -> float:
    """Cálculo manual con las fórmulas: paralelo = 1 - Π(1 - R_i), serie = Π R_i."""
    R_fw = 0.97
    R_psu = 0.90   # porque cada PSU falla 0.10
    R_fan = 0.95   # porque cada ventilador falla 0.05

    # 2 PSUs en paralelo: 1 - (1-0.90)^2 = 1 - 0.1^2 = 0.99
    R_alim = 1 - (1 - R_psu) ** 2

    # 3 ventiladores en paralelo: 1 - (1-0.95)^3 = 1 - 0.05^3 = 0.999875
    R_refri = 1 - (1 - R_fan) ** 3

    # Serie global
    R_total = R_fw * R_alim * R_refri  # ≈ 0.9601799625
    return R_fw, R_alim, R_refri, R_total


if __name__ == "__main__":
    # Cálculo con DBFs
    R_dbf = escenario_servidor_critico()

    # Cálculo manual (para verificar)
    R_fw, R_alim, R_refri, R_manual = calculo_manual()

    print("=== Cálculo manual ===")
    print(f"Firewall (R_fw)              = {R_fw:.6f}")
    print(f"Alimentación 2xPSU (paral.)  = {R_alim:.6f}  (1 - (1-0.90)^2)")
    print(f"Refrigeración 3xFAN (paral.) = {R_refri:.6f}  (1 - (1-0.95)^3)")
    print(f"Fiabilidad total (manual)    = {R_manual:.10f}")

    print("\n=== Con DBFs (función) ===")
    print(f"Fiabilidad total (DBF)       = {R_dbf:.10f}")

    # Verificación
    assert isclose(R_dbf, R_manual, rel_tol=1e-12, abs_tol=1e-12)

    # Probabilidad de que el servidor deje de funcionar en el fin de semana
    p_fallo = 1 - R_dbf
    print(f"\nProbabilidad de fallo (fin de semana): {p_fallo:.10f}  (~{p_fallo*100:.4f}%)")

    # Valores esperados de referencia:
    # R_alim = 0.99, R_refri = 0.999875, R_total ≈ 0.9601799625, fallo ≈ 0.0398200375

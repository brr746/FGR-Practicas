from __future__ import annotations
from typing import Dict, List, Any


DBF = Dict[str, Any]

def calcular_fiabilidad(S: DBF) -> float:
    """
    Calcula recursivamente la fiabilidad de un sistema definido como DBF.

    Estructura esperada por bloque (dict):
      - tipo: "simple" | "serie" | "paralelo"
      - R: float en [0,1] (solo para tipo "simple")
      - subcomp: list[DBF] (vacía para "simple"; no vacía para compuestos)

    Reglas:
      - Serie: R = Π R_i
      - Paralelo: R = 1 - Π (1 - R_i)

    Lanza ValueError si la estructura es inválida.
    """
    if not isinstance(S, dict):
        raise ValueError("El sistema debe ser un dict.")

    tipo = S.get("tipo")
    if tipo not in {"simple", "serie", "paralelo"}:
        raise ValueError("La clave 'tipo' debe ser 'simple', 'serie' o 'paralelo'.")

    if tipo == "simple":
        if "R" not in S:
            raise ValueError("Los componentes 'simple' requieren la clave 'R'.")
        R = float(S["R"])
        if not (0.0 <= R <= 1.0):
            raise ValueError("La fiabilidad R debe estar en [0,1].")
        # 'subcomp' puede venir vacío; se ignora para 'simple'
        return R

    # Para compuestos, necesitamos subcomp no vacío
    sub = S.get("subcomp")
    if not isinstance(sub, list) or len(sub) == 0:
        raise ValueError("Los bloques compuestos requieren una lista 'subcomp' no vacía.")

    # Calculamos recursivamente
    Rs: List[float] = [calcular_fiabilidad(x) for x in sub]

    if tipo == "serie":
        prod = 1.0
        for r in Rs:
            prod *= r
        return prod

    # tipo == "paralelo"
    q = 1.0
    for r in Rs:
        q *= (1.0 - r)
    return 1.0 - q


# (Opcional) Pequeños 'helpers' si queréis construir DBFs más legibles:
def simple(R: float) -> DBF:
    return dict(tipo="simple", R=float(R), subcomp=[])

def serie(*subs: DBF) -> DBF:
    return dict(tipo="serie", R=None, subcomp=list(subs))

def paralelo(*subs: DBF) -> DBF:
    return dict(tipo="paralelo", R=None, subcomp=list(subs))

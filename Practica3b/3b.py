import math
import pyagrum as gum

# ===============================================================
#  EJERCICIO 1: Propagación de probabilidades en un árbol de fallos
# ===============================================================

def propagacion(nodo: dict) -> None:
    if nodo["tipo"] == "evento" and nodo["hijos"] == []:
        return

    for h in nodo["hijos"]:
        propagacion(h)

    if nodo["tipo"] == "evento" and len(nodo["hijos"]) == 1:
        nodo["prob"] = nodo["hijos"][0]["prob"]
        return

    if nodo["tipo"] == "AND":
        p1 = nodo["hijos"][0]["prob"]
        p2 = nodo["hijos"][1]["prob"]
        nodo["prob"] = round(p1 * p2, 3)
        return

    if nodo["tipo"] == "OR":
        p1 = nodo["hijos"][0]["prob"]
        p2 = nodo["hijos"][1]["prob"]
        nodo["prob"] = round(1 - (1 - p1) * (1 - p2), 3)
        return


# ===============================================================
#  EJERCICIO 2
# ===============================================================

def nodos(nodo: dict) -> list:
    lista = [nodo]
    for h in nodo["hijos"]:
        lista.extend(nodos(h))
    return lista


# ===============================================================
#  EJERCICIO 3
# ===============================================================

def eventos(nodo: dict) -> list:
    return [n for n in nodos(nodo) if n["tipo"] == "evento"]


# ===============================================================
#  EJERCICIO 4
# ===============================================================

def evento_info(nodo: dict, nombre: str) -> tuple:
    for n in nodos(nodo):
        if n["tipo"] == "evento":
            for h in n["hijos"]:
                if h["tipo"] in ("AND", "OR"):
                    hijos_ev = h["hijos"]
                    nombres = [ev["nombre"] for ev in hijos_ev]
                    if nombre in nombres:
                        return (h["tipo"], hijos_ev[0]["nombre"], hijos_ev[1]["nombre"])
    return None


# ===============================================================
#  EJERCICIO 5
# ===============================================================

def transformar(nodo: dict) -> gum.BayesNet:
    bn = gum.BayesNet()
    ids = {}

    for n in nodos(nodo):
        nombre = n["nombre"] if n["nombre"] else f"X{id(n)}"
        ids[id(n)] = bn.add(nombre, 2)

    for n in nodos(nodo):
        for h in n["hijos"]:
            bn.addArc(ids[id(h)], ids[id(n)])

    for n in nodos(nodo):
        vid = ids[id(n)]

        if n["tipo"] == "evento" and n["prob"] is not None:
            bn.cpt(vid).fillWith([1 - n["prob"], n["prob"]])
            continue

        if len(n["hijos"]) == 2:
            cpt = bn.cpt(vid)
            for a in [0,1]:
                for b in [0,1]:
                    if n["tipo"] == "AND":
                        val = 1 if (a==1 and b==1) else 0
                    elif n["tipo"] == "OR":
                        val = 1 if (a==1 or b==1) else 0
                    else:
                        val = 0
                    cpt[(a,b)] = [1-val, val]

    return bn


# ===============================================================
#  EJERCICIO 6 – MODELO DEL SERVIDOR
# ===============================================================

def exp_fallo(t, beta):
    return round(1 - math.exp(-t/beta), 3)

def weibull_fallo(t, alpha, beta):
    return round(1 - math.exp(-(t/beta)**alpha), 3)

def construir_arbol_ej6():

    t = 1  # 1 año

    p_red    = exp_fallo(t, 10)
    p_cpu    = exp_fallo(t, 3)
    p_disco  = weibull_fallo(t, 1, 3)

    red = dict(tipo="evento", nombre="Red", prob=p_red, hijos=[])

    cpu1 = dict(tipo="evento", nombre="CPU1", prob=p_cpu, hijos=[])
    cpu2 = dict(tipo="evento", nombre="CPU2", prob=p_cpu, hijos=[])
    cpu_fail = dict(tipo="AND", nombre=None, prob=None, hijos=[cpu1, cpu2])

    d1 = dict(tipo="evento", nombre="D1", prob=p_disco, hijos=[])
    d2 = dict(tipo="evento", nombre="D2", prob=p_disco, hijos=[])
    d3 = dict(tipo="evento", nombre="D3", prob=p_disco, hijos=[])

    and12 = dict(tipo="AND", nombre=None, prob=None, hijos=[d1, d2])
    discos_fail = dict(tipo="AND", nombre=None, prob=None, hijos=[and12, d3])

    root = dict(tipo="OR", nombre="FalloServidor", prob=None, hijos=[
        red, cpu_fail, discos_fail
    ])

    return root


# ===============================================================
#  EJECUCIÓN
# ===============================================================

if __name__ == "__main__":
    arbol = construir_arbol_ej6()

    propagacion(arbol)
    print("Probabilidad total del fallo del servidor:", arbol["prob"])

    print("\nEventos encontrados:")
    for ev in eventos(arbol):
        print(ev["nombre"], ev["prob"])

    bn = transformar(arbol)
    print("\nNodos en la red bayesiana:", bn.names())

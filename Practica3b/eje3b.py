# fallos.py
import math
import pyagrum as gum

# ===============================================================
#  EJERCICIO 1: Propagación de probabilidades en un árbol de fallos
# ===============================================================

def propagacion(nodo: dict) -> None:
    # evento hoja
    if nodo["tipo"] == "evento" and nodo["hijos"] == []:
        return

    # primero propagar en hijos
    for h in nodo["hijos"]:
        propagacion(h)

    # evento con 1 hijo: copia probabilidad
    if nodo["tipo"] == "evento" and len(nodo["hijos"]) == 1:
        nodo["prob"] = nodo["hijos"][0]["prob"]
        return

    # AND con N hijos: producto
    if nodo["tipo"] == "AND":
        p = 1.0
        for h in nodo["hijos"]:
            p *= h["prob"]
        nodo["prob"] = round(p, 3)
        return

    # OR con N hijos: 1 - prod(1-pi)
    if nodo["tipo"] == "OR":
        q = 1.0
        for h in nodo["hijos"]:
            q *= (1 - h["prob"])
        nodo["prob"] = round(1 - q, 3)
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

import itertools
import pyagrum as gum

def transformar(nodo: dict) -> gum.BayesNet:
    bn = gum.BayesNet()
    ids = {}

    # 1) Crear variables
    for n in nodos(nodo):
        nombre = n["nombre"] if n["nombre"] else f"X{id(n)}"
        # Aseguramos nombres únicos si por alguna razón se repitieran, 
        # aunque tu lógica de nombres parece correcta.
        try:
            ids[id(n)] = bn.add(nombre, 2)
        except gum.AlreadyExists:
            ids[id(n)] = bn.idFromName(nombre)

    # 2) Crear arcos (hijo_arbol -> padre_arbol)
    for n in nodos(nodo):
        for h in n["hijos"]:
            bn.addArc(ids[id(h)], ids[id(n)])

    # 3) Rellenar CPTs
    for n in nodos(nodo):
        vid = ids[id(n)]
        cpt = bn.cpt(vid)
        num_parents = len(n["hijos"])
        
        # Limpiamos la CPT
        cpt.fillWith(0)

        # CASO 1: Nodo Hoja (0 padres/hijos en árbol)
        # Aquí sí usamos la probabilidad asignada.
        if num_parents == 0:
            p = n["prob"]
            # Si por error p fuera None en una hoja, asumimos 0 o lanzamos error
            if p is None: p = 0 
            cpt[:] = [1 - p, p]
            continue

        # Obtener los IDs de las variables padre para configurar la CPT correctamente
        parent_ids = [ids[id(h)] for h in n["hijos"]]
        parent_names = [bn.variable(pid).name() for pid in parent_ids]

        # CASO 2: Evento Intermedio (1 padre/hijo en árbol)
        # IMPORTANTE: Quitamos la condición 'n["prob"] is None' para evitar el bug
        if n["tipo"] == "evento" and num_parents == 1:
            # Copia determinista: Si hijo es 0 -> padre 0, Si hijo 1 -> padre 1
            # Usamos sintaxis de diccionario para seguridad
            cpt[{parent_names[0]: 0}] = [1, 0] # Estado 0 -> 0
            cpt[{parent_names[0]: 1}] = [0, 1] # Estado 1 -> 1
            continue

        # CASO 3: Puertas AND/OR (>= 2 padres)
        if n["tipo"] in ("AND", "OR") and num_parents >= 2:
            # Iteramos todas las combinaciones posibles de los padres (entradas de la puerta)
            for parents_state in itertools.product([0, 1], repeat=num_parents):
                # Calcular la salida lógica
                if n["tipo"] == "AND":
                    out = 1 if all(parents_state) else 0
                else:  # OR
                    out = 1 if any(parents_state) else 0
                
                # Crear el selector para asignar a la CPT de forma segura
                # Mapeamos: NombreDeVariablePadre -> Estado (0 o 1)
                selector = {name: state for name, state in zip(parent_names, parents_state)}
                
                # Asignamos la distribución [P(False), P(True)]
                cpt[selector] = [1 - out, out]
            continue

    return bn




# ===============================================================
#  EJERCICIO 6 – MODELO DEL SERVIDOR
# ===============================================================

def exp_fallo(t, beta):
    return round(1 - math.exp(-t / beta), 3)

def weibull_fallo(t, alpha, beta):
    return round(1 - math.exp(-(t / beta) ** alpha), 3)

def construir_arbol_ej6():
    t = 1  # 1 año

    p_red   = exp_fallo(t, 10)
    p_cpu   = exp_fallo(t, 3)
    p_disco = weibull_fallo(t, 1, 3)

    # Eventos hoja
    red = dict(tipo="evento", nombre="Red", prob=p_red, hijos=[])

    cpu1 = dict(tipo="evento", nombre="CPU1", prob=p_cpu, hijos=[])
    cpu2 = dict(tipo="evento", nombre="CPU2", prob=p_cpu, hijos=[])
    cpu_fail = dict(tipo="AND", nombre=None, prob=None, hijos=[cpu1, cpu2])
    cpu_event = dict(tipo="evento", nombre="FalloCPU", prob=None, hijos=[cpu_fail])

    d1 = dict(tipo="evento", nombre="D1", prob=p_disco, hijos=[])
    d2 = dict(tipo="evento", nombre="D2", prob=p_disco, hijos=[])
    d3 = dict(tipo="evento", nombre="D3", prob=p_disco, hijos=[])

    and12 = dict(tipo="AND", nombre=None, prob=None, hijos=[d1, d2])
    discos_fail = dict(tipo="AND", nombre=None, prob=None, hijos=[and12, d3])
    discos_event = dict(tipo="evento", nombre="FalloDiscos", prob=None, hijos=[discos_fail])

    # Puerta OR principal
    or_principal = dict(tipo="OR", nombre=None, prob=None, hijos=[red, cpu_event])

    # Como OR solo puede tener 2 hijos, anidamos para incluir discos_event
    or_total = dict(tipo="OR", nombre=None, prob=None, hijos=[or_principal, discos_event])

    # RAÍZ: debe ser evento (según enunciado)
    raiz = dict(tipo="evento", nombre="FalloServidor", prob=None, hijos=[or_total])
    return raiz


def prob_raiz_por_inferencia(bn: gum.BayesNet, nombre_raiz: str) -> float:
    ie = gum.LazyPropagation(bn)
    ie.makeInference()
    posterior = ie.posterior(nombre_raiz)  # distribución del nodo
    return float(posterior[1])  # estado 1 = "falla"

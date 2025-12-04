import pyAgrum as gum
import pyAgrum.lib.notebook as gnb

# ------------------------------------------
# 1. Crear el modelo bayesiano
# ------------------------------------------
bn = gum.BayesNet("RiesgoServidor")

# ------------------------------------------
# 2. Añadir nodos
# ------------------------------------------
# A1: Ataque (0=no, 1=sí)
A1 = bn.add(gum.LabelizedVariable("A1", "Ataque", 2)) 
# C: CortafuegosActivo (0=activo, 1=inactivo/actualizándose)
C  = bn.add(gum.LabelizedVariable("C", "CortafuegosActivo", 2))
# A2: AtaqueFiltrado (0=no pasa, 1=pasa ataque)
A2 = bn.add(gum.LabelizedVariable("A2", "AtaqueFiltrado", 2))
# SQ: SistemaDeRecuperacion (0=no activo, 1=activo)
SQ = bn.add(gum.LabelizedVariable("SQ", "SistemaDeRecuperacion", 2))
# F: FalloGrave (0=no, 1=sí)
F  = bn.add(gum.LabelizedVariable("F", "FalloGrave", 2))

# ------------------------------------------
# 3. Añadir aristas
# ------------------------------------------
bn.addArc(A1, A2)
bn.addArc(C, A2)
bn.addArc(A2, F)
bn.addArc(SQ, F)

# ------------------------------------------
# 4. Definir las probabilidades (CPTs)
# ------------------------------------------

# --- Nodo A1 (Ataque) ---
# 200 de 1000 son ataques -> 20% Sí, 80% No
bn.cpt("A1").fillWith([0.8, 0.2]) 

# --- Nodo C (Cortafuegos) ---
# Inactivo 6 min cada hora (6/60 = 0.1) -> 10% Inactivo, 90% Activo
bn.cpt("C").fillWith([0.9, 0.1]) 

# --- Nodo SQ (Sistema Recuperación) ---
# Funciona el 85% del tiempo
bn.cpt("SQ").fillWith([0.15, 0.85]) 

# --- Nodo A2 (Ataque Filtrado) ---
# Depende de A1 (Ataque) y C (Estado Cortafuegos)
cpt_A2 = bn.cpt("A2")
# Si NO hay ataque (A1=0), A2 es siempre 0 (no pasa nada)
cpt_A2[{"A1":0, "C":0}] = [1, 0] 
cpt_A2[{"A1":0, "C":1}] = [1, 0] 
# Si HAY ataque (A1=1):
# - Si Cortafuegos ACTIVO (C=0): Falla 1 de cada 4 (25% pasa) -> [0.75, 0.25]
cpt_A2[{"A1":1, "C":0}] = [0.75, 0.25]
# - Si Cortafuegos INACTIVO (C=1): Pasa siempre -> [0, 1]
cpt_A2[{"A1":1, "C":1}] = [0, 1]

# --- Nodo F (Fallo Grave) --- [CORREGIDO SEGÚN ENUNCIADO]
# Depende de A2 (Ataque Filtrado) y SQ (Sistema Recuperación)
cpt_F = bn.cpt("F")

# Si NO pasó ataque (A2=0), probabilidad de fallo es 0
cpt_F[{"A2":0, "SQ":0}] = [1, 0]
cpt_F[{"A2":0, "SQ":1}] = [1, 0]

# Si SÍ pasó ataque (A2=1):
# - Sin Sistema (SQ=0): "50% ataques suponen fallo grave" -> [0.5, 0.5]
cpt_F[{"A2":1, "SQ":0}] = [0.5, 0.5]
# - Con Sistema (SQ=1): "Evita la mitad de fallos graves".
#   La mitad de 0.5 es 0.25. Prob fallo = 0.25 -> [0.75, 0.25]
cpt_F[{"A2":1, "SQ":1}] = [0.75, 0.25]

# ------------------------------------------
# 5. Inferencia 1: Situación Normal
# ------------------------------------------
ie = gum.LazyPropagation(bn)
ie.makeInference()
p_fallo = ie.posterior("F")[1] # Probabilidad de F=1

print(f"Probabilidad de fallo grave (Escenario normal): {p_fallo:.4f}")

# ------------------------------------------
# 6. Inferencia 2: Cortafuegos Desconectado
# ------------------------------------------
ie.setEvidence({"C":1}) # C = inactivo (100% seguro)
ie.makeInference()
p_fallo_sin_cortafuegos = ie.posterior("F")[1]

print(f"Probabilidad de fallo grave (SIN cortafuegos): {p_fallo_sin_cortafuegos:.4f}")

# ------------------------------------------
# 7. Exportar para Hugin (Requisito de entrega)
# ------------------------------------------
# El enunciado pide entregar ficheros .net u .oobn
gum.saveBN(bn, "practica3a_grupo.net")
print("Modelo guardado como 'practica3a_grupo.net'")
import pyagrum as gum

# ------------------------------------------
# 1. Crear el modelo bayesiano
# ------------------------------------------
bn = gum.BayesNet("RiesgoServidor")

# ------------------------------------------
# 2. Añadir nodos
# ------------------------------------------
A1 = bn.add(gum.LabelizedVariable("A1", "Ataque", 2))          # 0=no, 1=sí
C  = bn.add(gum.LabelizedVariable("C", "Cortafuegos", 2))      # 0=activo, 1=inactivo
A2 = bn.add(gum.LabelizedVariable("A2", "AtaqueFiltrado", 2))  # 0=no pasa, 1=pasa
SQ = bn.add(gum.LabelizedVariable("SQ", "SistemaRecuperacion", 2))  # 0=no activo, 1=activo
F  = bn.add(gum.LabelizedVariable("F", "FalloGrave", 2))       # 0=no, 1=sí

# ------------------------------------------
# 3. Estructura (arcos)
# ------------------------------------------
bn.addArc(A1, A2)
bn.addArc(C, A2)
bn.addArc(A2, F)
bn.addArc(SQ, F)

# ------------------------------------------
# 4. CPTs (Tablas de Probabilidad)
# ------------------------------------------

# A1: 20% ataques
bn.cpt("A1").fillWith([0.8, 0.2])

# C: 90% activo, 10% inactivo
bn.cpt("C").fillWith([0.9, 0.1])

# SQ: 85% activo
bn.cpt("SQ").fillWith([0.15, 0.85])

# --- A2 depende de A1 y C ---
cpt_A2 = bn.cpt("A2")
# Si no hay ataque -> nunca pasa ataque
cpt_A2[{"A1":0, "C":0}] = [1, 0]
cpt_A2[{"A1":0, "C":1}] = [1, 0]
# Si hay ataque y firewall activo → 25% pasa
cpt_A2[{"A1":1, "C":0}] = [0.75, 0.25]
# Si hay ataque y firewall inactivo → pasa seguro
cpt_A2[{"A1":1, "C":1}] = [0, 1]

# --- F depende de A2 y SQ ---
cpt_F = bn.cpt("F")

# Si no pasa ataque → no hay fallo
cpt_F[{"A2":0, "SQ":0}] = [1, 0]
cpt_F[{"A2":0, "SQ":1}] = [1, 0]

# Si pasa ataque → 50% falla sin sistema, 25% con sistema
cpt_F[{"A2":1, "SQ":0}] = [0.5, 0.5]
cpt_F[{"A2":1, "SQ":1}] = [0.75, 0.25]

# ------------------------------------------
# 5. Inferencia NORMAL (sin evidencias)
# ------------------------------------------
ie = gum.LazyPropagation(bn)
ie.makeInference()
p_normal = ie.posterior("F")[1]

print(f"Probabilidad de fallo grave (NORMAL): {p_normal:.4f}")

# ------------------------------------------
# 6. Inferencia SIN CORTAFUEGOS (C=1)
# ------------------------------------------
ie = gum.LazyPropagation(bn)
ie.setEvidence({"C":1})
ie.makeInference()
p_sin_fw = ie.posterior("F")[1]

print(f"Probabilidad de fallo grave (SIN cortafuegos): {p_sin_fw:.4f}")

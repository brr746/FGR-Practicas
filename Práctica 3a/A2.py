import pyAgrum as gum
import pyAgrum.lib.notebook as gnb

# ------------------------------------------
# 1. Crear el modelo bayesiano vacío
# ------------------------------------------
bn = gum.BayesNet("RiesgoServidor")

# ------------------------------------------
# 2. Añadir nodos
# ------------------------------------------
A1 = bn.add(gum.LabelizedVariable("A1", "Ataque", 2))  # 0=no, 1=sí
C  = bn.add(gum.LabelizedVariable("C", "CortafuegosActivo", 2))
A2 = bn.add(gum.LabelizedVariable("A2", "AtaqueFiltrado", 2))
SQ = bn.add(gum.LabelizedVariable("SQ", "SistemaDeRecuperacion", 2))
F  = bn.add(gum.LabelizedVariable("F", "FalloGrave", 2))

# ------------------------------------------
# 3. Añadir aristas (estructura de la red)
# ------------------------------------------
bn.addArc(A1, A2)
bn.addArc(C, A2)
bn.addArc(A2, F)
bn.addArc(SQ, F)

# ------------------------------------------
# 4. Definir las probabilidades
# ------------------------------------------

# Nodo A1 (ataque)
bn.cpt("A1").fillWith([0.8, 0.2])   # no ataque = 0.8, ataque = 0.2

# Nodo C (cortafuegos activo)
bn.cpt("C").fillWith([0.9, 0.1])    # activo = 0.9, inactivo = 0.1

# Nodo SQ (sistema recuperación)
bn.cpt("SQ").fillWith([0.15, 0.85]) # no activo = 0.15, activo = 0.85

# Nodo A2 (dependiente de A1 y C)
# Orden: A1 (0=no,1=sí), C (0=activo,1=inactivo), A2 (0=no filtrado, 1=filtrado)
cpt_A2 = bn.cpt("A2")

cpt_A2[{"A1":0, "C":0}] = [1, 0]      # no ataque → no pasa
cpt_A2[{"A1":0, "C":1}] = [1, 0]      
cpt_A2[{"A1":1, "C":0}] = [0.75, 0.25]  # cortafuegos activo deja pasar 25%
cpt_A2[{"A1":1, "C":1}] = [0, 1]        # firewall inactivo → pasa siempre

# Nodo F (fallo grave)
# F depende de A2 y SQ
# Orden: A2(0,1), SQ(0,1), F(0=no,1=sí)
cpt_F = bn.cpt("F")

cpt_F[{"A2":0, "SQ":0}] = [1, 0]   # sin ataque filtrado → nunca hay fallo
cpt_F[{"A2":0, "SQ":1}] = [1, 0]

cpt_F[{"A2":1, "SQ":0}] = [0, 1]   # ataque filtrado + sin sistema recuperación → fallo seguro
cpt_F[{"A2":1, "SQ":1}] = [0.5, 0.5]   # ataque filtrado + sistema → mitad de fallos

# ------------------------------------------
# 5. Inferencia: probabilidad de fallo grave
# ------------------------------------------
ie = gum.LazyPropagation(bn)
ie.makeInference()

p_fallo = ie.posterior("F")[1]
print("Probabilidad de fallo grave:", p_fallo)

# ------------------------------------------
# 6. Caso alternativo: cortafuegos desconectado
# ------------------------------------------
ie.setEvidence({"C":1})   # C = inactivo
ie.makeInference()

p_fallo_sin_cortafuegos = ie.posterior("F")[1]
print("Probabilidad de fallo grave SIN cortafuegos:", p_fallo_sin_cortafuegos)

# main.py
from Práctica2b.B2 import rexp2, rweibull2

# Tiempo de operación
t = 2  # años

# --- 1️⃣ Sistema de alimentación ---
# 2 fuentes en paralelo, exponencial, esperanza de vida 5 años
beta_fuente = 5
R_fuente_unit = rexp2(t, beta_fuente)         # Fiabilidad de una fuente
R_fuentes = 1 - (1 - R_fuente_unit)**2        # Fallan solo si fallan ambas

# --- 2️⃣ Servidores de cálculo ---
# 3 servidores independientes, exponencial, esperanza 4 años
beta_servidor = 4
R_servidor_unit = rexp2(t, beta_servidor)
# El sistema funciona mientras haya al menos 1 servidor operativo
# Falla solo si fallan los 3
R_servidores = 1 - (1 - R_servidor_unit)**3

# --- 3️⃣ Sistema de respaldo de datos ---
# 4 discos en paralelo, Weibull α=2, β=2
alpha_disco = 2
beta_disco = 2
R_disco_unit = rweibull2(t, alpha_disco, beta_disco)
# Fallo solo si fallan los 4 discos
R_respaldo = 1 - (1 - R_disco_unit)**4

# --- Fiabilidad total del sistema ---
# Serie: el sistema funciona solo si todos funcionan
R_sistema = R_fuentes * R_servidores * R_respaldo

# --- Resultados ---
print("Fiabilidades después de 2 años de operación:\n")
print(f"Sistema de alimentación (2 en paralelo): {R_fuentes:.6f}")
print(f"Servidores de cálculo (3, falla si fallan los 3): {R_servidores:.6f}")
print(f"Sistema de respaldo (4 discos, falla si fallan los 4): {R_respaldo:.6f}")
print(f"\nFiabilidad total del sistema: {R_sistema:.6f}")

# --- Interpretación ---
subsistemas = {
    "Sistema de alimentación": R_fuentes,
    "Servidores de cálculo": R_servidores,
    "Sistema de respaldo": R_respaldo
}

# Subsistema más crítico = el de menor fiabilidad
critico = min(subsistemas, key=subsistemas.get)
print(f"\nSubsistema más crítico después de 2 años: {critico}")

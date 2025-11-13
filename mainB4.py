# main.py
from B2 import rexp2, rweibull2

# Tiempo de operación
t = 2  # años

# --- 1️⃣ Fuente de alimentación ---
# 2 fuentes en paralelo, exponencial, esperanza de vida 5 años
beta_fuente = 5
R_fuente_unit = rexp2(t, beta_fuente)
R_fuentes = 1 - (1 - R_fuente_unit)**2  # falla si ambas fallan

# --- 2️⃣ Servidores de cálculo ---
# 3 servidores, exponencial, esperanza de vida 4 años
beta_servidor = 4
R_servidor_unit = rexp2(t, beta_servidor)
# Subsystem falla si al menos 2 fallan: probabilidad de que 0 o 1 falle
R_servidores = R_servidor_unit**3 + 3 * R_servidor_unit**2 * (1 - R_servidor_unit)

# --- 3️⃣ Sistema de respaldo de datos ---
# 4 discos en paralelo, Weibull α=2, β=2
alpha_disco = 2
beta_disco = 2
R_disco_unit = rweibull2(t, alpha_disco, beta_disco)
R_respaldo = 1 - (1 - R_disco_unit)**4  # falla si los 4 discos fallan

# --- Fiabilidad total del sistema ---
R_sistema = R_fuentes * R_servidores * R_respaldo

# --- Resultados ---
print("Fiabilidades después de 2 años de operación:\n")
print(f"Fuentes de alimentación (2 en paralelo): {R_fuentes:.6f}")
print(f"Servidores de cálculo (3, falla si al menos 2 fallan): {R_servidores:.6f}")
print(f"Sistema de respaldo (4 discos, falla si los 4 fallan): {R_respaldo:.6f}")
print(f"\nFiabilidad total del sistema: {R_sistema:.6f}")

# --- Interpretación ---
subsistemas = {
    "Fuentes de alimentación": R_fuentes,
    "Servidores de cálculo": R_servidores,
    "Sistema de respaldo": R_respaldo
}

# Encontrar el subsistema más crítico (menor fiabilidad)
critico = min(subsistemas, key=subsistemas.get)
print(f"\nSubsistema más crítico después de 2 años: {critico}")

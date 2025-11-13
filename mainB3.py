# main.py
from B2 import rexp2, rweibull2

# --- Escenario ---
t = 1  # año

# 1️⃣ Tarjeta de red (exponencial, esperanza de vida 10 años)
beta_red = 10
R_red = rexp2(t, beta_red)

# 2️⃣ Procesadores (2 en paralelo, exponencial, esperanza de vida 3 años)
beta_cpu = 3
R_cpu_unit = rexp2(t, beta_cpu)
R_cpu = 1 - (1 - R_cpu_unit)**2  # falla si ambos procesadores fallan

# 3️⃣ Sistema de almacenamiento (3 discos en paralelo, Weibull α=1, β=3)
alpha_disk = 1
beta_disk = 3
R_disk_unit = rweibull2(t, beta_disk, alpha_disk)
R_disk = 1 - (1 - R_disk_unit)**3  # falla si los 3 discos fallan

# 4️⃣ Fiabilidad total del servidor
R_servidor = R_red * R_cpu * R_disk

# --- Resultados ---
print(f"Fiabilidad de la tarjeta de red después de {t} año(s): {R_red:.6f}")
print(f"Fiabilidad de los procesadores después de {t} año(s): {R_cpu:.6f}")
print(f"Fiabilidad del sistema de almacenamiento después de {t} año(s): {R_disk:.6f}")
print(f"\nFiabilidad total del servidor después de {t} año(s): {R_servidor:.6f}")

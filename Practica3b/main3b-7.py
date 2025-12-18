import pyagrum as gum
from eje3b import construir_arbol_ej7, propagacion, eventos, transformar, prob_raiz_por_inferencia
import math

def main():
    arbol = construir_arbol_ej7()

    # Propagar probabilidades en el árbol
    propagacion(arbol)
    print("=== Probabilidad total de fallo del servidor (árbol) ===")
    print(f"Fallo del servidor en 1 año: {arbol['prob']*100:.2f}%\n")

    # Mostrar todos los eventos hoja/intermedios
    print("=== Eventos encontrados (tipo=evento) ===")
    for ev in eventos(arbol):
        print(f"- {ev['nombre']}: {ev['prob']}")

    # Transformar a Red Bayesiana
    bn = transformar(arbol)

    # Probabilidad de fallo usando inferencia bayesiana
    p_bn = prob_raiz_por_inferencia(bn, "FalloServidor")
    print("\n=== Probabilidad de fallo del servidor (inferencia BN) ===")
    print(f"Fallo del servidor en 1 año: {p_bn*100:.2f}%\n")

    # Mostrar nombres de los nodos en la Red Bayesiana
    print("=== Nodos en la Red Bayesiana ===")
    print(bn.names())

if __name__ == "__main__":
    main()
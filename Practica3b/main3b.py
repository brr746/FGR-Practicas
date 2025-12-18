# main3b.py
import pyagrum as gum
from eje3b import construir_arbol_ej6, propagacion, eventos, transformar, prob_raiz_por_inferencia

def main():
    arbol = construir_arbol_ej6()

    propagacion(arbol)
    print("Probabilidad total de fallo del servidor (árbol):", arbol["prob"])

    print("\nEventos encontrados (tipo=evento):")
    for ev in eventos(arbol):
        print(f"- {ev['nombre']}: {ev['prob']}")

    bn = transformar(arbol)
    p_bn = prob_raiz_por_inferencia(bn, "FalloServidor")
    print("\nProbabilidad de fallo del servidor (inferencia BN):", round(p_bn, 6))

    print("\nNodos en la red bayesiana:", bn.names())

if __name__ == "__main__":
    main()

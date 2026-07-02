import networkx as nx

def ejecutar_girvan_newman(G, comunidades_objetivo=5):
    """
    Ejecuta el algoritmo de Girvan-Newman.
    Se detiene cuando el grafo se divide en la cantidad de 'comunidades_objetivo'.
    """
    print(f"\nEjecutando Girvan-Newman para encontrar {comunidades_objetivo} comunidades...")
    
    # comp es un generador que arroja tuplas de comunidades en cada corte
    comp = nx.community.girvan_newman(G)
    
    resultado_comunidades = []
    
    for comunidades in comp:
        # Cada iteración divide el grafo un poco más
        if len(comunidades) >= comunidades_objetivo:
            resultado_comunidades = [list(c) for c in comunidades]
            break
            
    print("¡Algoritmo finalizado con éxito!")
    return resultado_comunidades
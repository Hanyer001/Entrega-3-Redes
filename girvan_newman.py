import networkx as nx  # Importa la librería NetworkX para trabajar con grafos

def ejecutar_girvan_newman(G, comunidades_objetivo=5):
    """
    Ejecuta el algoritmo de Girvan-Newman.
    Se detiene cuando el grafo se divide en la cantidad de 'comunidades_objetivo'.
    """

    # Mensaje informativo indicando cuántas comunidades se buscan
    print(f"\nEjecutando Girvan-Newman para encontrar {comunidades_objetivo} comunidades...")
    
    # 'comp' es un generador que devuelve particiones del grafo progresivamente
    # En cada iteración elimina aristas con alta intermediación (betweenness)
    comp = nx.community.girvan_newman(G)
    
    resultado_comunidades = []  # Lista donde se almacenará el resultado final
    
    # Itera sobre cada partición generada por el algoritmo
    for comunidades in comp:
        # Cada iteración aumenta el número de comunidades (divide más el grafo)

        # Si ya alcanzamos o superamos la cantidad deseada de comunidades
        if len(comunidades) >= comunidades_objetivo:
            # Convierte cada comunidad (set) en lista
            resultado_comunidades = [list(c) for c in comunidades]
            break  # Detiene el algoritmo
    
    # Mensaje indicando que el proceso terminó correctamente
    print("¡Algoritmo finalizado con éxito!")
    
    return resultado_comunidades  # Retorna la lista de comunidades encontradas

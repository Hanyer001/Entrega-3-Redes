import networkx as nx  # Importa NetworkX para trabajar con grafos

def ejecutar_louvain(G):  # Define la función que ejecuta Louvain recibiendo un grafo como parámetro
    """
    Ejecuta el algoritmo de Louvain para detección de comunidades.
    Aprovecha los pesos (weight) de las aristas generados por el índice de Jaccard.
    """
    print("\nEjecutando algoritmo de Louvain...")  # Muestra un mensaje en pantalla antes de iniciar
    
    # nx.community.louvain_communities devuelve una lista de conjuntos (sets)
    # donde cada conjunto contiene los nodos que pertenecen a una comunidad
    # El parámetro weight='weight' indica que se tomarán en cuenta los pesos de las aristas
    comunidades = nx.community.louvain_communities(G, weight='weight')
    
    # Convierte cada conjunto en una lista para que el formato sea más fácil de manipular
    # y quede consistente con Girvan-Newman
    resultado_comunidades = [list(c) for c in comunidades]
    
    # Ordena las comunidades desde la más grande hasta la más pequeña
    resultado_comunidades.sort(key=len, reverse=True)
    
    # Imprime cuántas comunidades fueron detectadas automáticamente
    print(f"¡Louvain finalizado! Se detectaron {len(resultado_comunidades)} comunidades automáticamente.")
    
    # Retorna la lista final de comunidades
    return resultado_comunidades

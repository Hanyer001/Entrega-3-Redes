import networkx as nx

def ejecutar_louvain(G):
    """
    Ejecuta el algoritmo de Louvain para detección de comunidades.
    Aprovecha los pesos (weight) de las aristas generados por el índice de Jaccard.
    """
    print("\nEjecutando algoritmo de Louvain...")
    
    # nx.community.louvain_communities devuelve una lista de sets, 
    # donde cada set contiene los nodos de una comunidad.
    # Le indicamos que tome en cuenta el peso de la similitud.
    comunidades = nx.community.louvain_communities(G, weight='weight')
    
    # Convertir los sets a listas para mantener consistencia con Girvan-Newman
    resultado_comunidades = [list(c) for c in comunidades]
    
    # Ordenar las comunidades por tamaño (de la que tiene más artistas a la que tiene menos)
    resultado_comunidades.sort(key=len, reverse=True)
    
    print(f"¡Louvain finalizado! Se detectaron {len(resultado_comunidades)} comunidades automáticamente.")
    return resultado_comunidades
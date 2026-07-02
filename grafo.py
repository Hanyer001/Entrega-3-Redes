import pandas as pd
import networkx as nx
from itertools import combinations

def calcular_jaccard(lista_a, lista_b):
    set_a = set(lista_a)
    set_b = set(lista_b)
    interseccion = len(set_a.intersection(set_b))
    
    if interseccion == 0:
        return 0.0
        
    union = len(set_a.union(set_b))
    return interseccion / union

def construir_grafo(ruta_csv='top_400_artists_gn.csv', umbral_jaccard=0.6):
    df = pd.read_csv(ruta_csv)
    
    # Convertir el string de géneros de vuelta a lista de Python
    df['genres_list'] = df['genres'].apply(lambda x: [g.strip() for g in x.split(',') if g.strip()])
    
    G = nx.Graph()
    
    # 1. Añadir nodos
    for _, row in df.iterrows():
        G.add_node(row['id_artista'], name=row['name'], followers=row['followers'], genres=row['genres'])
        
    # 2. Añadir aristas basadas en Jaccard
    artistas = df[['id_artista', 'genres_list']].to_dict('records')
    
    for a, b in combinations(artistas, 2):
        jaccard = calcular_jaccard(a['genres_list'], b['genres_list'])
        
        # Si superan o igualan el umbral, creamos la conexión
        if jaccard >= umbral_jaccard:
            # Añadir el peso a la arista (útil para visualizaciones o análisis posteriores)
            G.add_edge(a['id_artista'], b['id_artista'], weight=jaccard)
            
    # 3. Eliminar nodos que quedaron totalmente aislados por la exigencia del filtro
    nodos_aislados = list(nx.isolates(G))
    G.remove_nodes_from(nodos_aislados)
    
    print(f"Grafo construido: {G.number_of_nodes()} nodos conectados y {G.number_of_edges()} aristas (Umbral: {umbral_jaccard}).")
    print(f"Se eliminaron {len(nodos_aislados)} artistas aislados.")
    
    return G
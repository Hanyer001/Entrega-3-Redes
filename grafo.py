import pandas as pd  # Importa Pandas para leer y manipular archivos CSV
import networkx as nx  # Importa NetworkX para crear y trabajar con grafos
from itertools import combinations  # Importa combinations para generar pares de artistas

def calcular_jaccard(lista_a, lista_b):  # Define una función para calcular la similitud de Jaccard
    set_a = set(lista_a)  # Convierte la primera lista en conjunto para eliminar duplicados
    set_b = set(lista_b)  # Convierte la segunda lista en conjunto para eliminar duplicados
    interseccion = len(set_a.intersection(set_b))  # Cuenta cuántos géneros comparten
    
    if interseccion == 0:  # Si no tienen géneros en común
        return 0.0  # Devuelve 0 como similitud
        
    union = len(set_a.union(set_b))  # Calcula cuántos géneros únicos hay entre ambas listas
    return interseccion / union  # Devuelve el índice de Jaccard

def construir_grafo(ruta_csv='top_400_artists_gn.csv', umbral_jaccard=0.6):  # Define la función para construir el grafo
    df = pd.read_csv(ruta_csv)  # Lee el archivo CSV con los artistas
    
    # Convertir el string de géneros de vuelta a lista de Python
    df['genres_list'] = df['genres'].apply(lambda x: [g.strip() for g in x.split(',') if g.strip()])  # Convierte el texto de géneros en lista
    
    G = nx.Graph()  # Crea un grafo no dirigido vacío
    
    # 1. Añadir nodos
    for _, row in df.iterrows():  # Recorre cada fila del DataFrame
        G.add_node(row['id_artista'], name=row['name'], followers=row['followers'], genres=row['genres'])  # Agrega cada artista como nodo con atributos
        
    # 2. Añadir aristas basadas en Jaccard
    artistas = df[['id_artista', 'genres_list']].to_dict('records')  # Convierte las columnas necesarias en una lista de diccionarios
    
    for a, b in combinations(artistas, 2):  # Genera todas las combinaciones posibles de dos artistas
        jaccard = calcular_jaccard(a['genres_list'], b['genres_list'])  # Calcula la similitud entre ambos artistas
        
        # Si superan o igualan el umbral, creamos la conexión
        if jaccard >= umbral_jaccard:  # Revisa si la similitud es suficiente
            # Añadir el peso a la arista (útil para visualizaciones o análisis posteriores)
            G.add_edge(a['id_artista'], b['id_artista'], weight=jaccard)  # Agrega la arista con su peso
            
    # 3. Eliminar nodos que quedaron totalmente aislados por la exigencia del filtro
    nodos_aislados = list(nx.isolates(G))  # Obtiene los nodos sin conexiones
    G.remove_nodes_from(nodos_aislados)  # Elimina esos nodos del grafo
    
    print(f"Grafo construido: {G.number_of_nodes()} nodos conectados y {G.number_of_edges()} aristas (Umbral: {umbral_jaccard}).")  # Muestra resumen del grafo
    print(f"Se eliminaron {len(nodos_aislados)} artistas aislados.")  # Muestra cuántos aislados se eliminaron
    
    return G  # Retorna el grafo construido

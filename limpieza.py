import pandas as pd  # Importa Pandas para manejar datos en forma de tablas
import ast  # Importa ast para convertir texto con listas en listas reales de Python
import networkx as nx  # Importa NetworkX para crear y trabajar con grafos
from itertools import combinations  # Importa combinations para generar pares de artistas

# 1. Cargar el dataset original
df = pd.read_csv('nodes.csv')  # Lee el archivo CSV y lo guarda en un DataFrame

# 2. Limpiar 'name'
df['name'] = df['name'].astype(str).str.strip()  # Convierte 'name' a texto y elimina espacios innecesarios
df = df[df['name'] != 'nan']  # Elimina filas donde el nombre quedó como 'nan'

# 3. Limpiar 'followers' (convertir a número y manejar nulos)
df['followers'] = pd.to_numeric(df['followers'], errors='coerce').fillna(0)  # Convierte followers a número; si falla, pone 0

# 4. Función para extraer géneros
def get_genres_list(g_str):  # Define una función para transformar el texto de géneros en lista
    if pd.isna(g_str):  # Verifica si el valor está vacío o nulo
        return []  # Si está vacío, devuelve una lista vacía
    try:  # Intenta ejecutar el bloque siguiente
        g_list = ast.literal_eval(g_str)  # Convierte el texto a una estructura de Python
        if isinstance(g_list, list):  # Verifica si el resultado es una lista
            return [str(g).strip() for g in g_list if str(g).strip()]  # Limpia cada género y elimina vacíos
    except:  # Si ocurre un error al evaluar el texto
        pass  # Ignora el error y sigue con el procesamiento manual
    cleaned = str(g_str).strip()  # Convierte el valor a texto y elimina espacios
    return [cleaned] if cleaned else []  # Devuelve una lista con el texto si no está vacío

df['genres_list'] = df['genres'].apply(get_genres_list)  # Aplica la función a la columna genres y guarda el resultado

# =========================================================
# 5. APLICACIÓN DE FILTROS ESTRATÉGICOS
# =========================================================

# A. Solo artistas con 3 o más géneros (automáticamente elimina los de 0)
df = df[df['genres_list'].apply(len) >= 3].copy()  # Filtra filas que tengan al menos 3 géneros

# B. Ordenar por seguidores de mayor a menor y tomar solo el TOP 400
df = df.sort_values(by='followers', ascending=False).head(400).copy()  # Ordena por seguidores y toma los primeros 400

# C. Volver a formato de texto para el CSV limpio
df['genres'] = df['genres_list'].apply(lambda x: ", ".join(x))  # Convierte la lista de géneros a texto separado por comas

# D. Crear id_artista secuencial (1 al 400)
df.insert(0, 'id_artista', range(1, len(df) + 1))  # Inserta una columna ID al inicio con números consecutivos

# Guardar el CSV definitivo (añadiendo 'followers' para tener contexto)
df_final = df[['id_artista', 'name', 'followers', 'genres']]  # Selecciona solo las columnas que se guardarán
df_final.to_csv('top_400_artists_gn.csv', index=False)  # Guarda el DataFrame en un nuevo CSV sin índice
print("Archivo 'top_400_artists_gn.csv' guardado con éxito. Nodos:", len(df_final))  # Muestra cuántos nodos se guardaron

# =========================================================
# 6. CREACIÓN DEL GRAFO 
# =========================================================
G = nx.Graph()  # Crea un grafo no dirigido vacío

# Agregar nodos
for _, row in df_final.iterrows():  # Recorre cada fila del DataFrame
    G.add_node(row['id_artista'], name=row['name'], followers=row['followers'], genres=row['genres'])  # Agrega un nodo con atributos

# Agregar aristas (conexiones por género)
df_exploded = df[['id_artista', 'genres_list']].explode('genres_list')  # Separa la lista de géneros en filas individuales
edges_set = set()  # Crea un conjunto para evitar aristas repetidas

for genre, group in df_exploded.groupby('genres_list'):  # Agrupa por cada género
    artistas = group['id_artista'].tolist()  # Obtiene la lista de artistas que tienen ese género
    if len(artistas) > 1:  # Verifica que haya más de un artista con ese género
        for pair in combinations(artistas, 2):  # Genera todas las combinaciones posibles de dos artistas
            edges_set.add((min(pair), max(pair)))  # Agrega la arista ordenada para evitar duplicados

G.add_edges_from(edges_set)  # Agrega todas las aristas al grafo

print(f"Total de artistas (Nodos): {G.number_of_nodes()}")  # Imprime el total de nodos del grafo
print(f"Total de conexiones (Aristas): {G.number_of_edges()}")  # Imprime el total de aristas del grafo

# Opcional: Exportar el grafo en formato GML para visualizarlo en Gephi
nx.write_gml(G, "grafo_artistas_top400.gml")  # Guarda el grafo en formato GML

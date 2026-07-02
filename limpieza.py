import pandas as pd
import ast
import networkx as nx
from itertools import combinations

# 1. Cargar el dataset original
df = pd.read_csv('nodes.csv')

# 2. Limpiar 'name'
df['name'] = df['name'].astype(str).str.strip()
df = df[df['name'] != 'nan']

# 3. Limpiar 'followers' (convertir a número y manejar nulos)
df['followers'] = pd.to_numeric(df['followers'], errors='coerce').fillna(0)

# 4. Función para extraer géneros
def get_genres_list(g_str):
    if pd.isna(g_str):
        return []
    try:
        g_list = ast.literal_eval(g_str)
        if isinstance(g_list, list):
            return [str(g).strip() for g in g_list if str(g).strip()]
    except:
        pass
    cleaned = str(g_str).strip()
    return [cleaned] if cleaned else []

df['genres_list'] = df['genres'].apply(get_genres_list)

# =========================================================
# 5. APLICACIÓN DE FILTROS ESTRATÉGICOS
# =========================================================
# A. Solo artistas con 3 o más géneros (automáticamente elimina los de 0)
df = df[df['genres_list'].apply(len) >= 3].copy()

# B. Ordenar por seguidores de mayor a menor y tomar solo el TOP 400
df = df.sort_values(by='followers', ascending=False).head(400).copy()

# C. Volver a formato de texto para el CSV limpio
df['genres'] = df['genres_list'].apply(lambda x: ", ".join(x))

# D. Crear id_artista secuencial (1 al 400)
df.insert(0, 'id_artista', range(1, len(df) + 1))

# Guardar el CSV definitivo (añadiendo 'followers' para tener contexto)
df_final = df[['id_artista', 'name', 'followers', 'genres']]
df_final.to_csv('top_400_artists_gn.csv', index=False)
print("Archivo 'top_400_artists_gn.csv' guardado con éxito. Nodos:", len(df_final))

# =========================================================
# 6. CREACIÓN DEL GRAFO 
# =========================================================
G = nx.Graph()

# Agregar nodos
for _, row in df_final.iterrows():
    G.add_node(row['id_artista'], name=row['name'], followers=row['followers'], genres=row['genres'])

# Agregar aristas (conexiones por género)
df_exploded = df[['id_artista', 'genres_list']].explode('genres_list')
edges_set = set()

for genre, group in df_exploded.groupby('genres_list'):
    artistas = group['id_artista'].tolist()
    if len(artistas) > 1:
        for pair in combinations(artistas, 2):
            edges_set.add((min(pair), max(pair)))

G.add_edges_from(edges_set)

print(f"Total de artistas (Nodos): {G.number_of_nodes()}")
print(f"Total de conexiones (Aristas): {G.number_of_edges()}")

# Opcional: Exportar el grafo en formato GML para visualizarlo en Gephi
nx.write_gml(G, "grafo_artistas_top400.gml")
"""
Script para exportar todos los datos necesarios del grafo y comunidades
a un archivo JSON que el demo.html pueda consumir directamente.
"""
import json  # Permite trabajar con archivos en formato JSON
from grafo import construir_grafo  # Importa función personalizada para construir el grafo desde CSV
from girvan_newman import ejecutar_girvan_newman  # (No se usa aquí directamente) implementación propia de Girvan-Newman
from louvain import ejecutar_louvain  # Importa función para ejecutar el algoritmo de Louvain
import networkx as nx  # Librería para manejo de grafos


def main():
    umbral = 0.6  # Define el umbral de similitud Jaccard para crear conexiones entre nodos

    # Construye el grafo usando el CSV y el umbral definido
    G = construir_grafo(ruta_csv='top_400_artists_gn.csv', umbral_jaccard=umbral)

    # ---- Datos del grafo ----
    nodes_data = []  # Lista donde se guardarán los nodos en formato JSON

    # Recorre cada nodo junto con sus atributos
    for nodo in G.nodes(data=True):
        nodes_data.append({
            "id": str(nodo[0]),  # ID del nodo (convertido a string)
            "name": nodo[1].get("name", ""),  # Nombre del nodo (si existe)
            "followers": int(nodo[1].get("followers", 0)),  # Cantidad de seguidores (default 0)
            "genres": nodo[1].get("genres", "")  # Géneros musicales asociados
        })

    edges_data = []  # Lista donde se guardarán las aristas

    # Recorre cada arista con sus atributos (peso, etc.)
    for u, v, d in G.edges(data=True):
        edges_data.append({
            "source": str(u),  # Nodo origen
            "target": str(v),  # Nodo destino
            "weight": round(d.get("weight", 0), 4)  # Peso de la arista (redondeado a 4 decimales)
        })

    # ---- Girvan-Newman con pasos intermedios ----
    print("\nGenerando pasos de Girvan-Newman...")  # Mensaje en consola

    comp = nx.community.girvan_newman(G)  # Generador que produce particiones progresivas del grafo

    gn_steps = []  # Lista para almacenar cada paso del algoritmo

    # Itera sobre cada partición generada
    for i, comunidades in enumerate(comp):
        # Convierte cada comunidad a lista de strings
        step_communities = [list(map(str, c)) for c in comunidades]

        gn_steps.append(step_communities)  # Guarda el paso actual

        print(f"  Paso {i+1}: {len(comunidades)} comunidades")  # Muestra número de comunidades

        # Detiene cuando se alcanzan al menos 10 comunidades
        if len(comunidades) >= 10:
            break

    # ---- Louvain ----
    comunidades_louvain = ejecutar_louvain(G)  # Ejecuta algoritmo de Louvain

    # Convierte comunidades a listas de strings
    louvain_result = [list(map(str, c)) for c in comunidades_louvain]

    # ---- Empaquetar todo ----
    export = {
        "umbral_jaccard": umbral,  # Umbral usado
        "num_nodos": G.number_of_nodes(),  # Total de nodos
        "num_aristas": G.number_of_edges(),  # Total de aristas
        "nodes": nodes_data,  # Lista de nodos
        "edges": edges_data,  # Lista de aristas
        "gn_steps": gn_steps,  # Pasos de Girvan-Newman
        "louvain": louvain_result  # Resultado de Louvain
    }

    # Escribe los datos en un archivo JSON
    with open("graph_data.json", "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False)  # Guarda sin escapar caracteres especiales

    # Mensajes finales de resumen
    print(f"\n✅ Archivo 'graph_data.json' generado exitosamente.")
    print(f"   Nodos: {G.number_of_nodes()}, Aristas: {G.number_of_edges()}")
    print(f"   Pasos GN guardados: {len(gn_steps)}")
    print(f"   Comunidades Louvain: {len(louvain_result)}")


# Punto de entrada del script
if __name__ == "__main__":
    main()  # Ejecuta la función principal

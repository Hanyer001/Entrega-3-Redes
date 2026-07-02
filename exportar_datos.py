"""
Script para exportar todos los datos necesarios del grafo y comunidades
a un archivo JSON que el demo.html pueda consumir directamente.
"""
import json
from grafo import construir_grafo
from girvan_newman import ejecutar_girvan_newman
from louvain import ejecutar_louvain
import networkx as nx

def main():
    umbral = 0.6
    G = construir_grafo(ruta_csv='top_400_artists_gn.csv', umbral_jaccard=umbral)

    # ---- Datos del grafo ----
    nodes_data = []
    for nodo in G.nodes(data=True):
        nodes_data.append({
            "id": str(nodo[0]),
            "name": nodo[1].get("name", ""),
            "followers": int(nodo[1].get("followers", 0)),
            "genres": nodo[1].get("genres", "")
        })

    edges_data = []
    for u, v, d in G.edges(data=True):
        edges_data.append({
            "source": str(u),
            "target": str(v),
            "weight": round(d.get("weight", 0), 4)
        })

    # ---- Girvan-Newman con pasos intermedios ----
    print("\nGenerando pasos de Girvan-Newman...")
    comp = nx.community.girvan_newman(G)
    gn_steps = []
    for i, comunidades in enumerate(comp):
        step_communities = [list(map(str, c)) for c in comunidades]
        gn_steps.append(step_communities)
        print(f"  Paso {i+1}: {len(comunidades)} comunidades")
        if len(comunidades) >= 10:
            break

    # ---- Louvain ----
    comunidades_louvain = ejecutar_louvain(G)
    louvain_result = [list(map(str, c)) for c in comunidades_louvain]

    # ---- Empaquetar todo ----
    export = {
        "umbral_jaccard": umbral,
        "num_nodos": G.number_of_nodes(),
        "num_aristas": G.number_of_edges(),
        "nodes": nodes_data,
        "edges": edges_data,
        "gn_steps": gn_steps,
        "louvain": louvain_result
    }

    with open("graph_data.json", "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False)

    print(f"\n✅ Archivo 'graph_data.json' generado exitosamente.")
    print(f"   Nodos: {G.number_of_nodes()}, Aristas: {G.number_of_edges()}")
    print(f"   Pasos GN guardados: {len(gn_steps)}")
    print(f"   Comunidades Louvain: {len(louvain_result)}")

if __name__ == "__main__":
    main()

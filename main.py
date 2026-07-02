from grafo import construir_grafo
from girvan_newman import ejecutar_girvan_newman
from louvain import ejecutar_louvain

def main():
    # 1. Construir el grafo
    umbral = 0.6
    G = construir_grafo(ruta_csv='top_400_artists_gn.csv', umbral_jaccard=umbral)
    
    # ==========================================
    # 2. EJECUTAR GIRVAN-NEWMAN (Top-Down)
    # ==========================================
    num_comunidades = 5
    comunidades_gn = ejecutar_girvan_newman(G, comunidades_objetivo=num_comunidades)
    
    print("\n--- RESULTADOS GIRVAN-NEWMAN ---")
    for i, com in enumerate(comunidades_gn, 1):
        nombres = [G.nodes[nodo]['name'] for nodo in com[:5]]
        print(f"Comunidad {i} ({len(com)} artistas): {', '.join(nombres)}...")

    # ==========================================
    # 3. EJECUTAR LOUVAIN (Bottom-Up)
    # ==========================================
    # Nota: Louvain decide automáticamente la cantidad óptima de comunidades
    comunidades_louvain = ejecutar_louvain(G)
    
    print("\n--- RESULTADOS LOUVAIN ---")
    for i, com in enumerate(comunidades_louvain, 1):
        nombres = [G.nodes[nodo]['name'] for nodo in com[:5]]
        print(f"Comunidad {i} ({len(com)} artistas): {', '.join(nombres)}...")

    # 4. Mensaje final
    print("\n-> Ambos algoritmos ejecutados con éxito. El entorno está listo para que construyas tu HTML.")

if __name__ == "__main__":
    main()
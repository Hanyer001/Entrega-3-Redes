from grafo import construir_grafo  # Importa la función construir_grafo desde el archivo grafo.py
from girvan_newman import ejecutar_girvan_newman  # Importa la función ejecutar_girvan_newman desde girvan_newman.py
from louvain import ejecutar_louvain  # Importa la función ejecutar_louvain desde louvain.py

def main():  # Define la función principal del programa
    # 1. Construir el grafo
    umbral = 0.6  # Define el umbral de Jaccard que se usará para crear conexiones
    G = construir_grafo(ruta_csv='top_400_artists_gn.csv', umbral_jaccard=umbral)  # Construye el grafo desde el CSV
    
    # ==========================================
    # 2. EJECUTAR GIRVAN-NEWMAN (Top-Down)
    # ==========================================
    num_comunidades = 5  # Define la cantidad de comunidades objetivo para Girvan-Newman
    comunidades_gn = ejecutar_girvan_newman(G, comunidades_objetivo=num_comunidades)  # Ejecuta el algoritmo
    
    print("\n--- RESULTADOS GIRVAN-NEWMAN ---")  # Imprime un encabezado para los resultados
    for i, com in enumerate(comunidades_gn, 1):  # Recorre cada comunidad con un contador desde 1
        nombres = [G.nodes[nodo]['name'] for nodo in com[:5]]  # Toma hasta 5 nombres de artistas de la comunidad
        print(f"Comunidad {i} ({len(com)} artistas): {', '.join(nombres)}...")  # Muestra el tamaño y algunos nombres

    # ==========================================
    # 3. EJECUTAR LOUVAIN (Bottom-Up)
    # ==========================================
    # Nota: Louvain decide automáticamente la cantidad óptima de comunidades
    comunidades_louvain = ejecutar_louvain(G)  # Ejecuta Louvain sobre el grafo
    
    print("\n--- RESULTADOS LOUVAIN ---")  # Imprime encabezado de resultados
    for i, com in enumerate(comunidades_louvain, 1):  # Recorre cada comunidad con un contador desde 1
        nombres = [G.nodes[nodo]['name'] for nodo in com[:5]]  # Toma hasta 5 nombres de artistas por comunidad
        print(f"Comunidad {i} ({len(com)} artistas): {', '.join(nombres)}...")  # Imprime resumen de la comunidad

    # 4. Mensaje final
    print("\n-> Ambos algoritmos ejecutados con éxito. El entorno está listo para que construyas tu HTML.")  # Mensaje final

if __name__ == "__main__":  # Verifica si el archivo se está ejecutando directamente
    main()  # Llama a la función principal
    

import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.estruturas.grafo import GrafoAdjacencia
from src.processamento.pln import processar_textos
from src.algoritimos.Kruskal import executar_kruskal

def auditar_agrupamentos():
    caminho_json = os.path.join(os.path.dirname(__file__), '..', 'data', 'noticias.json')
    with open(caminho_json, 'r', encoding='utf-8') as f:
        noticias = json.load(f)

    print("Iniciando auditoria analítica dos dados...")
    arestas = processar_textos(noticias)
    grafo = GrafoAdjacencia(limite_distancia=0.80)
    for id1, id2, dist in arestas:
        grafo.adicionar_aresta(id1, id2, dist)
    
    topicos, _ = executar_kruskal(grafo, 3)

    # Definição do Gabarito Baseado na Geração de Dados (IDs 1-19: Esportes, 20-38: Economia, 39-57: Tecnologia, 58-60: Nós Ponte)
    gabarito = {
        "Esportes": set(range(1, 20)),
        "Economia": set(range(20, 39)),
        "Tecnologia": set(range(39, 58)),
        "Nos_Ponte": {58, 59, 60}
    }

    print("\n📊 RELATÓRIO DE ACURÁCIA DE CLUSTERIZAÇÃO")
    for i, cluster in enumerate(topicos):
        cluster_set = set(cluster)
        
        # Identifica a qual tema principal este cluster pertence pegando a maior interseção
        match_esportes = len(cluster_set.intersection(gabarito["Esportes"]))
        match_economia = len(cluster_set.intersection(gabarito["Economia"]))
        match_tecnologia = len(cluster_set.intersection(gabarito["Tecnologia"]))
        
        # Define o rótulo do cluster baseado na predominância
        if match_esportes > 10: tema = "Esportes"
        elif match_economia > 10: tema = "Economia"
        elif match_tecnologia > 10: tema = "Tecnologia"
        else: tema = "Indefinido/Misto"

        # Identifica os nós ponte que foram engolidos por este cluster
        pontes_absorvidos = cluster_set.intersection(gabarito["Nos_Ponte"])

        print(f"\nCluster {i+1} classificado como: {tema.upper()}")
        print(f" -> Notícias alvo corretas capturadas: {len(cluster_set.intersection(gabarito[tema]))} de 19")
        if pontes_absorvidos:
            print(f" -> Nós Ponte absorvidos por gravidade semântica: {pontes_absorvidos}")

if __name__ == "__main__":
    auditar_agrupamentos()
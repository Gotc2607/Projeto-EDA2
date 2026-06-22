import json
import os
from src.estruturas.grafo import GrafoAdjacencia
from src.processamento.pln import processar_textos
from src.algoritimos.Kruskal import executar_kruskal
from src.estruturas.tabela_hash import TabelaHash
import json
import os
from src.estruturas.grafo import GrafoAdjacencia
from src.algoritimos.Kruskal import executar_kruskal

# 1. Pessoa 5 lê o JSON
caminho_json = os.path.join(os.path.dirname(__file__), 'data', 'noticias.json')
with open(caminho_json, 'r', encoding='utf-8') as f:
    noticias = json.load(f)

# 2. Pessoa 2 limpa os textos e calcula as distâncias
print("[1/4] Processando textos e calculando distâncias de Jaccard...")
arestas_calculadas = processar_textos(noticias)
print(f"      Total de combinações analisadas: {len(arestas_calculadas)}")

# 3. Pessoa 1 e 4 alimentam o Grafo
print("[2/4] Montando o Grafo e aplicando Filtro de Densidade (Corte de 0.80)...")
grafo = GrafoAdjacencia(limite_distancia=0.80)
for id1, id2, distancia in arestas_calculadas:
    grafo.adicionar_aresta(id1, id2, distancia)
print(f"      Arestas válidas no grafo após o filtro: {len(grafo.obter_todas_arestas())}")

# 4. Pessoa 3 roda o algoritmo
num_topicos_desejados = 3
print(f"[3/4] Executando Kruskal (Union-Find) para formar {num_topicos_desejados} tópicos...")
topicos, mst_cortada = executar_kruskal(grafo, num_topicos_desejados)

# 5. Apresentação Analítica 
print("\n" + "="*60)
print("🎯 RESULTADO DO AGRUPAMENTO (COMUNIDADES ENCONTRADAS)")
print("="*60)
for i, topico in enumerate(topicos):
    print(f"\nTópico {i + 1} (Contém {len(topico)} notícias):")
    # Ordenamos os IDs para facilitar a sua visualização e conferência
    print(f"IDs: {sorted(topico)}")
print("="*60 + "\n")

# 6. Integração da Tabela Hash para busca O(1)
print("[4/4] Alimentando Tabela Hash para busca O(1)...")
tabela_noticias = TabelaHash()
for nt in noticias:
    tabela_noticias.inserir(nt['titulo'], nt['id'])

print("\n" + "="*60)
print("🔍 TESTE DE BUSCA O(1) NA TABELA HASH")
print("="*60)
# Simulando um usuário buscando pelo título exato de uma notícia
titulo_busca = "Mercado financeiro cai com decisão do banco sobre juros"
id_encontrado = tabela_noticias.buscar(titulo_busca)

if id_encontrado:
    print(f"Sucesso! O título '{titulo_busca}' corresponde ao ID {id_encontrado}.")
else:
    print("Notícia não encontrada.")
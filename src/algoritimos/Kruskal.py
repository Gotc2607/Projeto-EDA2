from src.estruturas.union_find import UnionFind
from src.estruturas.grafo import GrafoAdjacencia

def executar_kruskal(grafo: GrafoAdjacencia, num_topicos: int) -> tuple[list[list[int]], list[tuple[float, int, int]]]:
    """
    Executa o algoritmo de Kruskal para construir a Árvore Geradora Mínima (MST)
    e dividir o portal em 'num_topicos' grupos (clusters/editorias).
    
    :param grafo: Instância do GrafoAdjacencia (criado pela Pessoa 1)
    :param num_topicos: Quantidade desejada de clusters (ex: 5 editorias).
    :return: Uma tupla (lista_de_topicos, mst_final_cortada)
             Onde lista_de_topicos é uma lista de listas de IDs de notícias.
    """
    
    # 1. Extrair e ordenar todas as arestas O(E log V)
    # A função obter_todas_arestas retorna (distancia, u, v)
    arestas = grafo.obter_todas_arestas()
    
    # O Python usa Timsort, que ordena as tuplas pelo primeiro elemento (distância).
    # Como queremos da menor para a maior distância, um simples sort() resolve em O(E log E),
    # o que equivale a O(E log V) para grafos.
    arestas.sort()

    # Extrair os vértices
    vertices = grafo.obter_todos_vertices()
    if not vertices:
        return [], []

    # O Union-Find da Pessoa 4 pressupõe IDs inteiros de 0 a (tamanho - 1).
    # Criamos mapeamentos de/para caso os IDs das notícias não sejam contíguos ou comecem de 1.
    id_para_indice = {id_noticia: i for i, id_noticia in enumerate(vertices)}
    indice_para_id = {i: id_noticia for i, id_noticia in enumerate(vertices)}
    
    n_vertices = len(vertices)
    
    # Instanciar a estrutura Union-Find
    uf = UnionFind(n_vertices)

    # Armazena as arestas que comporão a Árvore Geradora Mínima
    mst_completa = []
    
    # Para detectar o "Efeito Encadeamento" (nós que atuam como super hubs ou pontes)
    grau_mst = {id_noticia: 0 for id_noticia in vertices}

    # 2. Percorrer a lista ordenada de arestas
    for distancia, u, v in arestas:
        idx_u = id_para_indice[u]
        idx_v = id_para_indice[v]
        
        # O método union da Pessoa 4 já faz o "find" e só une se forem de grupos diferentes,
        # retornando True se a união foi feita, e False se já pertenciam ao mesmo grupo (evita ciclos).
        if uf.union(idx_u, idx_v):
            mst_completa.append((distancia, u, v))
            grau_mst[u] += 1
            grau_mst[v] += 1

    # Destaque de Ponto de Atenção: Efeito Encadeamento (Clusterização e Nós Ponte)
    # Procuramos por nós que conectaram muitas outras notícias
    limite_grau = max(4, int(n_vertices * 0.15)) # Critério empírico: 15% dos nós ou no mínimo 4 arestas
    nos_ponte = [node for node, grau in grau_mst.items() if grau >= limite_grau]
    
    if nos_ponte:
        print("\n" + "="*60)
        print("⚠️ AVISO DE CLUSTERIZAÇÃO: EFEITO ENCADEAMENTO DETECTADO ⚠️")
        print(f"Os nós (notícias) {nos_ponte} possuem um grau muito alto na MST.")
        print("Eles podem ser notícias genéricas atuando como 'ponte' entre assuntos diferentes (ex: política e esportes juntos).")
        print("RECOMENDAÇÃO: Avise a Pessoa 2 para ser mais rigorosa no 'Ponto de Corte' (diminuir limite_distancia) ou isole essas notícias.")
        print("="*60 + "\n")

    # 3. Remover as arestas mais pesadas para formar os clusters
    # Usamos o Union-Find da Pessoa 4 para ver quantos tópicos o grafo formou naturalmente
    topicos_formados_naturalmente = uf.quantidade_de_topicos()
    
    arestas_a_remover = num_topicos - topicos_formados_naturalmente
    
    if arestas_a_remover > 0 and len(mst_completa) >= arestas_a_remover:
        mst_cortada = mst_completa[:-arestas_a_remover]
    else:
        # O limite_distancia já separou os clusters de forma perfeita (ou além do necessário)
        mst_cortada = mst_completa

    # Para obtermos os tópicos resultantes finais após o corte,
    # reconstruímos as conexões em um novo Union-Find usando apenas as arestas que sobraram.
    uf_final = UnionFind(n_vertices)
    for distancia, u, v in mst_cortada:
        uf_final.union(id_para_indice[u], id_para_indice[v])

    # Coletar os clusters formados e mapear os índices de volta para os IDs originais
    grupos_indices = uf_final.obter_topicos()
    
    topicos_finais = []
    for grupo in grupos_indices:
        # Recupera os IDs reais
        topico = [indice_para_id[idx] for idx in grupo]
        topicos_finais.append(topico)
        
    return topicos_finais, mst_cortada

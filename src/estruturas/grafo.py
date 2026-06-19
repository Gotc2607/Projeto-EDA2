class GrafoAdjacencia:
    def __init__(self, limite_distancia: float = 0.80):
        """
        Inicializa o Grafo estruturado em Lista de Adjacência do zero.
        
        :param limite_distancia: Distância máxima permitida para criar uma aresta.
                                 Como distancia = 1 - similaridade, se a similaridade 
                                 for menor que 0.20 (distância > 0.80), a aresta é 
                                 automaticamente rejeitada para evitar o Grafo Denso.
        """
        # Dicionário nativo: Chave = ID do Vértice (int), Valor = Lista de conexões
        self.lista_adj: dict[int, list[dict]] = {}
        self.limite_distancia = limite_distancia

    def adicionar_vertice(self, id_noticia: int) -> None:
        """Adiciona uma nova notícia (vértice) ao grafo, se ainda não existir."""
        if id_noticia not in self.lista_adj:
            self.lista_adj[id_noticia] = []

    def adicionar_aresta(self, id1: int, id2: int, distancia: float) -> None:
        """
        Adiciona uma conexão bidirecional entre duas notícias com um peso (distância).
        Aplica o filtro de segurança contra o problema do Grafo Denso.
        """
        # TRAVA DE SEGURANÇA: Se a distância for muito grande (notícias muito diferentes),
        # nós barramos a criação da aresta para poupar memória e tempo de processamento.
        if distancia > self.limite_distancia:
            return

        # Garante que ambos os vértices existam na estrutura antes de ligá-los
        self.adicionar_vertice(id1)
        self.adicionar_vertice(id2)

        # Como o grafo é não-direcionado, a relação de similaridade é mútua (u -> v e v -> u)
        # Verificação rápida para evitar arestas duplicadas na lista de adjacência
        if not any(conexao['vizinho'] == id2 for conexao in self.lista_adj[id1]):
            self.lista_adj[id1].append({'vizinho': id2, 'distancia': distancia})
            self.lista_adj[id2].append({'vizinho': id1, 'distancia': distancia})

    def obter_vizinhos(self, id_noticia: int) -> list[dict]:
        """Retorna a lista de adjacência de um vértice específico."""
        return self.lista_adj.get(id_noticia, [])

    def obter_todos_vertices(self) -> list[int]:
        """Retorna uma lista com os IDs de todos os vértices presentes no grafo."""
        return list(self.lista_adj.keys())

    def obter_todas_arestas(self) -> list[tuple[float, int, int]]:
        """
        Extrai e retorna todas as arestas únicas do grafo no formato (distancia, u, v).
        Esta função é o contrato de integração com a Pessoa 3 (Kruskal), pois ele
        precisa dessa lista exata para ordenar as conexões do menor para o maior custo.
        """
        arestas = []
        visitadas = set()

        for u in self.lista_adj:
            for conexao in self.lista_adj[u]:
                v = conexao['vizinho']
                dist = conexao['distancia']

                # Como o grafo é não-direcionado, a aresta (1, 2) é a mesma que (2, 1).
                # Usamos uma tupla ordenada para garantir que vamos rastrear e retornar cada aresta apenas uma vez.
                aresta_id = tuple(sorted((u, v)))
                if aresta_id not in visitadas:
                    visitadas.add(aresta_id)
                    arestas.append((dist, u, v))
                    
        return arestas
class UnionFind:
    def __init__(self, tamanho):
        """
        Estrutura de dados auxiliar 2: Conjuntos Disjuntos.
        Otimizado com Compressão de Caminho e União por Tamanho.
        """
        self.pai = [i for i in range(tamanho)]
        self.tamanho = [1] * tamanho

    def find(self, i):
        """Encontra a raiz da notícia (Compressão de Caminho)."""
        if self.pai[i] == i:
            return i
        
        self.pai[i] = self.find(self.pai[i])
        return self.pai[i]

    def union(self, i, j):
        """Une dois grupos de notícias. Retorna False se formar ciclo."""
        raiz_i = self.find(i)
        raiz_j = self.find(j)

        # Se já estão no mesmo grupo (tópico), barra a união para não dar ciclo no Kruskal
        if raiz_i == raiz_j:
            return False

        # União por tamanho para manter a árvore balanceada
        if self.tamanho[raiz_i] < self.tamanho[raiz_j]:
            self.pai[raiz_i] = raiz_j
            self.tamanho[raiz_j] += self.tamanho[raiz_i]
        else:
            self.pai[raiz_j] = raiz_i
            self.tamanho[raiz_i] += self.tamanho[raiz_j]

        return True
    
    def obter_topicos(self):
        """
        Varre o Union-Find e agrupa os IDs das notícias que pertencem à mesma raiz.
        Retorna uma lista de listas, onde cada sublista é uma Editoria (Tópico) do portal.
        """
        topicos = {}
        # Varre todas as notícias para ver quem é o "chefe" delas
        for i in range(len(self.pai)):
            raiz = self.find(i)
            if raiz not in topicos:
                topicos[raiz] = []
            topicos[raiz].append(i)
            
        # Retorna apenas os grupos formados (ignorando as chaves do dicionário interno)
        return list(topicos.values())
    
    def quantidade_de_topicos(self):
        """Retorna quantos tópicos distintos existem atualmente no grafo."""
        raizes_unicas = set(self.find(i) for i in range(len(self.pai)))
        return len(raizes_unicas)
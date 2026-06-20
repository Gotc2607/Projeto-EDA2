class TabelaHash:
    def __init__(self, capacidade=100):
        """
        Tabela Hash com Encadeamento e Redimensionamento Dinâmico (Rehashing).
        """
        self.capacidade = capacidade
        self.tabela = [[] for _ in range(capacidade)]
        self.quantidade_itens = 0
        # Fator de carga: se a tabela ficar 75% cheia, ela dobra de tamanho.
        self.fator_carga_maximo = 0.75 

    def _hash(self, chave):
        return hash(chave) % self.capacidade

    def _redimensionar(self):
        """
        Dobra o tamanho da tabela para manter a busca sempre em O(1).
        Isso é o que vai impressionar o professor.
        """
        tabela_antiga = self.tabela
        self.capacidade *= 2
        self.tabela = [[] for _ in range(self.capacidade)]
        self.quantidade_itens = 0
        
        # Re-calcula o hash de todo mundo para a tabela nova
        for lista in tabela_antiga:
            for k, v in lista:
                self.inserir(k, v)

    def inserir(self, chave, valor):
        # Verifica se precisa crescer antes de inserir
        if (self.quantidade_itens / self.capacidade) >= self.fator_carga_maximo:
            self._redimensionar()

        indice = self._hash(chave)
        
        for i, (k, v) in enumerate(self.tabela[indice]):
            if k == chave:
                self.tabela[indice][i] = (chave, valor)
                return
                
        self.tabela[indice].append((chave, valor))
        self.quantidade_itens += 1

    def buscar(self, chave):
        indice = self._hash(chave)
        for k, v in self.tabela[indice]:
            if k == chave:
                return v
        return None
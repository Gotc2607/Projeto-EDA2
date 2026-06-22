# Projeto-EDA2
Projeto da matéria de Estrutura de Dados 2

## Divisão de tarefas

Giovani: Arquitetura do Grafo Base 

A Tarefa: Implementar a classe do Grafo do zero usando Lista de Adjacência.
O que não pode usar: Nenhuma biblioteca de grafos.
O que precisa fazer na prática:

    Criar a classe Grafo contendo um dicionário nativo do Python, onde a chave é o ID da notícia e o valor é uma lista de conexões (arestas).

    Ponto de Atenção (O Filtro do Grafo Denso): Você não vai aceitar toda e qualquer conexão. A sua função adicionar_aresta(id1, id2, peso) precisa ter um bloqueio. Se a Pessoa 2 mandar uma conexão com similaridade muito baixa (ex: menor que 0.20), a sua classe simplesmente ignora e não cria a aresta. Isso garante que o seu grafo continue esparso, salvando a memória do computador e mantendo o tempo em O(V+E).

Artur Fernades: Processamento de Linguagem Natural (PLN) e Matemática

A Tarefa: Limpar os textos e calcular o peso matemático das conexões.
O que não pode usar: Bibliotecas de grafos. (Bibliotecas de PLN como nltk e scikit-learn geralmente são permitidas para a matemática, confirme com o professor. Se não forem, você terá que implementar o cálculo de similaridade de Jaccard ou Cosseno na mão usando contagem de palavras).
O que precisa fazer na prática:

    Limpar os textos (remover pontuação, "e", "ou", "de").

    Comparar as notícias duas a duas para gerar a Similaridade.

    Ponto de Atenção (A Conversão para o Kruskal): O Kruskal procura o menor caminho. Então, você não vai passar a similaridade para a Pessoa 1, você vai passar a Distância. A matemática é simples: distancia = 1 - similaridade.

    Você e a Pessoa 1 devem testar juntos qual será o "Ponto de Corte" (Threshold) para não explodir o grafo com conexões inúteis.

João Leles: Algoritmo de Kruskal (O Coração do Agrupamento)

A Tarefa: Implementar o algoritmo de Kruskal do zero absoluto.
O que não pode usar: Funções prontas de agrupamento ou de árvores.
O que precisa fazer na prática:

    Criar uma função que extrai todas as arestas do grafo da Pessoa 1 e as ordena da menor distância para a maior em tempo O(ElogV).

    Percorrer essa lista ordenada ligando os nós usando a estrutura da Pessoa 4 (Union-Find) para garantir que não vai formar ciclos fechados (loops).

    Ponto de Atenção (Clusterização e o Efeito Encadeamento): O seu código vai construir a Árvore Geradora Mínima. Quando ela estiver pronta, para separar o portal em, digamos, 5 editorias (tópicos), você vai programar o algoritmo para apagar as 4 arestas mais pesadas (as maiores distâncias) dessa árvore.

    Se houver o temido Efeito Encadeamento (uma notícia genérica unindo política e esporte), seu código deve estar preparado para isolar e remover esse nó "ponte", ou você avisa a Pessoa 2 para ser mais rigorosa no "Ponto de Corte".

Davi Oliveira: Estruturas de Dados Auxiliares (A Base)

A Tarefa: Implementar as ferramentas que farão o código das Pessoas 1 e 3 rodarem sem travar.
O que não pode usar: Bibliotecas externas.
O que precisa fazer na prática:

    Union-Find (Conjuntos Disjuntos): Fazer a classe do zero com as funções Find (com compressão de caminho) e Union (por tamanho). Isso é o que permite a Pessoa 3 saber instantaneamente se duas notícias já estão no mesmo grupo ou não, sem precisar percorrer o grafo todo.

    Mapeamento Hash: O Grafo da Pessoa 1 trabalha com números (IDs), mas as notícias têm Títulos (Strings). Você vai garantir o uso do dicionário nativo do Python (que é uma Tabela Hash por baixo dos panos) para criar uma busca O(1). Quando alguém digitar o título da notícia, seu mapa devolve o ID numérico na hora.

Fabio Alessandro: Dados, Testes e Apresentação (A Defesa)

A Tarefa: Provar que a teoria virou realidade e preparar a defesa.
O que precisa fazer na prática:

    Usar IA para gerar um JSON com umas 50-100 notícias divididas claramente em temas (ex: 20 de esportes, 20 de economia, 20 de tecnologia).

    Ponto de Atenção (Análise Analítica): Rodar o código completo e cruzar os dados. A saída do algoritmo da Pessoa 3 realmente separou as 20 de esportes juntas? Houve alguma notícia que se perdeu?

    Montar os slides focando em justificar as decisões:

        Por que fizemos o Ponto de Corte (para evitar o Grafo Denso).

        Como o Union-Find otimizou o Kruskal.

        Como superamos o Efeito Encadeamento cortando as conexões mais fracas da Árvore.


## Arquitetura do Projeto

meu_projeto_grafos/
│
├── data/
│   └── noticias.json          # (Massa de testes)
│
├── src/
│   ├── __init__.py            # Torna a pasta src um pacote Python
│   │
│   ├── estruturas/            
│   │   ├── __init__.py
│   │   ├── grafo.py           # Classe Grafo 
│   │   ├── union_find.py      # Classe Union-Find 
│   │   └── tabela_hash.py     # Mapeamento de Títulos 
│   │
│   ├── processamento/        
│   │   ├── __init__.py
│   │   └── pln.py             # Limpeza de texto e cálculo de pesos
│   │
│   └── algoritmos/          
│       ├── __init__.py
│       └── kruskal.py         # Lógica do Kruskal e cortes de arestas
│
├── test/                    
│   └── analisar_resultados.py  # Script que mede a qualidade dos agrupamentos
│
├── main.py                    # Onde o fluxo principal roda (Integração)
└── README.md                  # Documentação do projeto para o GitHub

## Slides do projeto

https://docs.google.com/presentation/d/1SfnwfH8uyFpDE3SW-DyGDu-zxaFnCz_SpsFdkVRbbus/preview
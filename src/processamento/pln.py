# src/processamento/pln.py
import string

def limpar_texto(texto: str) -> set[str]:
    """
    Remove pontuações, converte o texto para minúsculas, divide em palavras
    e filtra conectivos comuns (stop words) como 'e', 'ou', 'de', 'a', 'o', etc.
    Retorna um conjunto (set) de palavras únicas.
    """
    # 1. Converter para minúsculas
    texto = texto.lower()
    
    # 2. Remover pontuações usando a tabela nativa do Python
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    
    # 3. Separar em palavras individuais
    palavras = texto.split()
    
    # 4. Lista de Stop Words (palavras vazias que não trazem contexto ao tema)
    stop_words = {
        'e', 'ou', 'de', 'do', 'da', 'em', 'um', 'uma', 'os', 'as', 
        'o', 'a', 'com', 'para', 'por', 'que', 'no', 'na', 'ao', 'aos'
    }
    
    # 5. Filtrar as palavras mantendo apenas as relevantes
    palavras_limpas = {palavra for palavra in palavras if palavra not in stop_words}
    
    return palavras_limpas


def calcular_similaridade_jaccard(set1: set[str], set2: set[str]) -> float:
    """
    Calcula o índice de Jaccard entre dois conjuntos de palavras.
    Jaccard = (interseção) / (união)
    """
    if not set1 or not set2:
        return 0.0
        
    intersecao = set1.intersection(set2)
    uniao = set1.union(set2)
    
    return len(intersecao) / len(uniao)


def processar_textos(noticias: list[dict]) -> list[tuple[int, int, float]]:
    """
    Recebe uma lista de notícias, compara todas duas a duas (combinação),
    calcula a similaridade, converte para distância e retorna uma lista de arestas prontas.
    
    Formato esperado de cada notícia: {'id': int, 'titulo': str, 'conteudo': str}
    Retorna uma lista de tuplas: (id1, id2, distancia)
    """
    arestas_calculadas = []
    n = len(noticias)
    
    # Pré-processa e limpa o texto de todas as notícias uma única vez para otimizar tempo
    noticias_limpas = []
    for nt in noticias:
        # Combinamos título e conteúdo para ter mais palavras contextuais para a análise
        texto_completo = f"{nt['titulo']} {nt.get('conteudo', '')}"
        noticias_limpas.append({
            'id': nt['id'],
            'palavras': limpar_texto(texto_completo)
        })
    
    # Compara as notícias duas a duas (Garante complexidade controlada evitando duplicidade)
    for i in range(n):
        for j in range(i + 1, n):
            id1 = noticias_limpas[i]['id']
            id2 = noticias_limpas[j]['id']
            
            # Calcula a semelhança textual
            similaridade = calcular_similaridade_jaccard(
                noticias_limpas[i]['palavras'], 
                noticias_limpas[j]['palavras']
            )
            
            # CONVERSÃO PARA O KRUSKAL: distancia = 1 - similaridade
            # Quanto mais parecidas as notícias, menor será a distância (tendendo a 0)
            distancia = 1.0 - similaridade
            
            arestas_calculadas.append((id1, id2, distancia))
            
    return arestas_calculadas
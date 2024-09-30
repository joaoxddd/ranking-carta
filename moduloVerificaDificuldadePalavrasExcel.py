import spacy
import pandas as pd
import re

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_lg")

# Lista de palavras relacionadas ao consumo de serviços online que não penalizam a nota (exceções)
palavras_excecao = [
    "access", "sign", "login", "logout", "click", "select", "continue", "proceed",
    "verify", "download", "submit", "review", "confirm", "attach", "upload",
    "create", "register", "choose", "complete", "pdf", "user", "link", "app", "apple", "google"
]

# Lista de palavras técnicas (jurídicas ou científicas) reais
palavras_tecnicas = [
    "sistema de gestão de formulários", "metodologia de pesquisa",
    "análise estatística", "dados empíricos", "modelo de dados", "protocolo de pesquisa",
    "evidência científica", "cláusula contratual", "eficácia jurídica", "compliance", "diligência",
    "asseguramento", "requisitos técnicos", "análise de viabilidade", "impacto regulatório", 
    "propriedade intelectual", "mandato", "intimação", "jurisprudência", "acórdão", 
    "sentença", "coisa julgada", "trânsito em julgado"
]

# Conjuntos para armazenar palavras difíceis e palavras em inglês encontradas
palavras_dificeis_encontradas = set()
palavras_ingles_encontradas = set()

# Função auxiliar para detectar palavras em inglês que não estão nas exceções
def contem_palavra_ingles(token):
    return token.is_alpha and token.lang_ == "en" and token.text not in palavras_excecao

# Função para avaliar critérios com base em palavras técnicas e palavras em inglês
def avaliar_criterios(texto):
    if not texto.strip():
        return 0, ""

    doc = nlp(texto.lower())  # Processa o texto com Spacy

    # Critério: Simplicidade (palavras em inglês e técnicas)
    palavras_tecnicas_usadas = [token.text for token in doc if token.text in palavras_tecnicas]
    palavras_em_ingles = [token.text for token in doc if contem_palavra_ingles(token)]
    
    # Acumula palavras técnicas e palavras em inglês encontradas
    palavras_dificeis_encontradas.update(palavras_tecnicas_usadas)
    palavras_ingles_encontradas.update(palavras_em_ingles)

    # Pontuação com base nas palavras encontradas
    simplicidade = 5 if len(palavras_tecnicas_usadas) == 0 and len(palavras_em_ingles) == 0 else 2.5
    
    # Criar observações se houver palavras penalizadas
    observacoes = []
    if len(palavras_tecnicas_usadas) > 0:
        observacoes.append(f"Uso de palavras técnicas: {palavras_tecnicas_usadas}")
    if len(palavras_em_ingles) > 0:
        observacoes.append(f"Uso de palavras em inglês: {palavras_em_ingles}")

    return simplicidade, "; ".join(observacoes) if observacoes else "Todos os critérios atendidos"

# Função para calcular a pontuação final com base na média das pontuações
def calcular_pontuacao_final(pontuacoes):
    if not pontuacoes:
        return 0  # Nenhuma pontuação para avaliar

    return sum(pontuacoes) / len(pontuacoes)  # Retorna a média das pontuações

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RankingCarta.xlsx')

# Inicializar a coluna de observações
df_saida['Obs Dificuldade Palavras'] = ""

# Avaliar cada coluna relevante e calcular a média das notas
for idx, row in df_entrada.iterrows():
    pontuacoes = []
    observacoes_gerais = []

    for coluna in ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]:
        if pd.notnull(row[coluna]):
            texto_coluna = str(row[coluna]).lower()  # Convertendo o texto da coluna para minúsculas
            nota, observacao = avaliar_criterios(texto_coluna)
            pontuacoes.append(nota)
            if observacao:  # Adicionar a observação apenas se ela não for vazia
                observacoes_gerais.append(f"{coluna}: {observacao}")

    # Calcular a pontuação final com base na média das pontuações
    pontuacao_final = calcular_pontuacao_final(pontuacoes)

    # Atualizar a coluna de notas e observações no arquivo de saída
    df_saida.at[idx, 'Nota Dificuldade Palavras'] = pontuacao_final
    df_saida.at[idx, 'Obs Dificuldade Palavras'] = "; ".join(observacoes_gerais) if observacoes_gerais else ""

# Salvar o arquivo atualizado
df_saida.to_excel('RankingCarta.xlsx', index=False)

# Printar palavras difíceis e palavras em inglês encontradas
print("\nDicionário de Palavras Difíceis Encontradas:")
print(sorted(palavras_dificeis_encontradas))

print("\nPalavras em Inglês Encontradas:")
print(sorted(palavras_ingles_encontradas))

print("\nArquivo atualizado com sucesso!")
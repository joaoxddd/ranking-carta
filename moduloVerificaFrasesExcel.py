import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_lg")

# Função para verificar se uma frase indica uma única ação
def unica_acao(frase):
    doc = nlp(frase)
    
    # Verificar se há mais de um verbo principal (ROOT)
    verbos_raiz = [token for token in doc if token.dep_ == "ROOT" and token.pos_ == "VERB"]
    
    conj_apos_verbo = False
    for token in doc:
        if token.pos_ == "CCONJ":  # Se for uma conjunção coordenativa
            next_token = token.nbor(1) if token.i + 1 < len(doc) else None
            if next_token and next_token.pos_ == "VERB":
                # Verificar se os verbos estão conectados por uma relação de dependência
                if next_token.head != token.head:
                    conj_apos_verbo = True
                    break

    return len(verbos_raiz) == 1 and not conj_apos_verbo

# Função para verificar se a frase está na forma direta (verbo no início)
def forma_direta(frase):
    doc = nlp(frase)
    if len(doc) > 0 and doc[0].pos_ == "VERB":  # Verifica se a primeira palavra é um verbo
        return True
    return False

# Função para calcular a pontuação com base nos critérios fornecidos
def avaliar_frase(frase):
    # Converter a frase para minúsculas
    frase = frase.lower()
    
    doc = nlp(frase)
    pontuacao = 0
    observacoes = []

    # Critério 1: Frases com no máximo 10 palavras
    if len(doc) <= 10:
        pontuacao += 2
    else:
        observacoes.append(f"Frase com mais de 10 palavras ({len(doc)} palavras)")
        pontuacao += 0  # Frases com mais de 10 palavras recebem 0 pontos

    # Critério 2: Frase indica uma única ação
    if unica_acao(frase):
        pontuacao += 1
    else:
        observacoes.append("Frase com mais de uma ação")

    # Critério 3: Frase na forma direta (verbo no início)
    if forma_direta(frase):
        pontuacao += 1
    else:
        observacoes.append("Frase não está na forma direta")

    return pontuacao, observacoes

# Função para calcular a média das pontuações obtidas
def calcular_media_pontuacoes(pontuacoes):
    if not pontuacoes:
        return 0
    return sum(pontuacoes) / len(pontuacoes)

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RankingCarta.xlsx')

# Colunas para serem analisadas
colunas_para_avaliar = ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]

# Inicializar a coluna de observações
df_saida['Obs Frases'] = ""

# Avaliar cada serviço nas colunas especificadas
for idx, row in df_entrada.iterrows():
    pontuacoes = []
    observacoes_gerais = []

    for coluna in colunas_para_avaliar:
        if pd.notnull(row[coluna]):
            frase = str(row[coluna]).lower()
            pontuacao, observacoes = avaliar_frase(frase)
            pontuacoes.append(pontuacao)
            if observacoes:
                observacoes_gerais.append(f"{coluna}: {', '.join(observacoes)}")

    # Calcular a média das pontuações das frases
    media_pontuacao = calcular_media_pontuacoes(pontuacoes)

    # Atualizar a coluna de notas e observações no arquivo de saída
    df_saida.at[idx, 'Nota Frases'] = media_pontuacao
    df_saida.at[idx, 'Obs Nota Frases'] = "; ".join(observacoes_gerais) if observacoes_gerais else "Todos os critérios atendidos"

# Salvar o arquivo atualizado
df_saida.to_excel('RankingCarta.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
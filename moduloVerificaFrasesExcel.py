import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

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
    doc = nlp(frase)
    pontuacao = 0
    
    # Critério 1: Frases com no máximo 10 palavras
    if len(doc) <= 10:
        pontuacao += 2
    else:
        pontuacao += 0

    # Critério 2: Frase indica uma única ação
    if unica_acao(frase):
        pontuacao += 1
    else:
        pontuacao += 0

    # Critério 3: Frase na forma direta (verbo no início)
    if forma_direta(frase):
        pontuacao += 1
    else:
        pontuacao += 0
    
    return pontuacao

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx')

# Colunas para serem analisadas
colunas_para_avaliar = ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]

# Converter a coluna de notas para float, caso ainda não esteja
df_saida['Nota moduloVerificaFrases.py'] = df_saida['Nota moduloVerificaFrases.py'].astype(float)

# Avaliar cada serviço nas colunas especificadas
for idx, row in df_entrada.iterrows():
    nota_total = 0
    for coluna in colunas_para_avaliar:
        if pd.notnull(row[coluna]):
            nota_total += avaliar_frase(str(row[coluna]))

    # Atualizar a coluna de saída correspondente ao índice
    df_saida.at[idx, 'Nota moduloVerificaFrases.py'] = nota_total

# Salvar o arquivo atualizado
df_saida.to_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
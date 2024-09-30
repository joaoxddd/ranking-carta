import spacy
import pandas as pd
import re

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_lg")

# Expressão regular para detectar e remover URLs
url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

# Expressão regular para detectar e remover e-mails
email_pattern = re.compile(r'\S+@\S+')

# Função para remover URLs e e-mails de um texto
def remover_urls_emails(texto):
    texto = re.sub(url_pattern, '', texto)  # Remove URLs
    texto = re.sub(email_pattern, '', texto)  # Remove e-mails
    return texto

# Função para avaliar tempos verbais e pronomes em pessoa/grau
def avaliar_tempo_verbal_pessoa(texto):
    # Remover URLs e e-mails antes da avaliação
    texto_limpo = remover_urls_emails(texto)
    
    # Converter o texto para minúsculas
    texto_limpo = texto_limpo.lower()
    
    doc = nlp(texto_limpo)
    pontuacao = 5  # Nota máxima inicial
    verbo_pronome_encontrado = False
    observacoes = []

    for token in doc:
        # Verificar verbos e pronomes
        if token.pos_ == "VERB" or token.pos_ == "PRON":
            verbo_pronome_encontrado = True
            pessoa = token.morph.get("Person")  # Identificar a pessoa (1ª, 2ª ou 3ª)
            numero = token.morph.get("Number")  # Identificar o número (Singular/Plural)

            # Atribuição de pontuação conforme as regras:
            if pessoa == ["2"] and numero == ["Sing"]:
                observacoes.append(f"Verbo/pronome na 2ª pessoa singular: {token.text}")
                pontuacao = min(pontuacao, 5)
            elif pessoa == ["3"] and numero == ["Sing"]:
                observacoes.append(f"Verbo/pronome na 3ª pessoa singular: {token.text}")
                pontuacao = min(pontuacao, 5)
            elif pessoa == ["2"] and numero == ["Plur"]:
                observacoes.append(f"Verbo/pronome na 2ª pessoa plural: {token.text}")
                pontuacao = min(pontuacao, 3)
            elif pessoa == ["3"] and numero == ["Plur"]:
                observacoes.append(f"Verbo/pronome na 3ª pessoa plural: {token.text}")
                pontuacao = min(pontuacao, 3)
            elif pessoa == ["1"] and numero == ["Sing"]:
                observacoes.append(f"Verbo/pronome na 1ª pessoa singular: {token.text}")
                pontuacao = min(pontuacao, 1)
            elif pessoa == ["1"] and numero == ["Plur"]:
                observacoes.append(f"Verbo/pronome na 1ª pessoa plural: {token.text}")
                pontuacao = min(pontuacao, 0)

    # Caso nenhum verbo ou pronome seja identificado, retorna a pontuação máxima
    if not verbo_pronome_encontrado:
        observacoes.append("Nenhum verbo ou pronome identificado")
        return 5, observacoes

    return pontuacao, observacoes

# Função para calcular a média das pontuações obtidas por vários campos
def calcular_media_pontuacoes(pontuacoes):
    if not pontuacoes:
        return 0
    return sum(pontuacoes) / len(pontuacoes)

# Carregar os arquivos
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RankingCarta.xlsx')

# Colunas para serem analisadas
colunas_para_avaliar = ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]

# Inicializar a coluna de observações
df_saida['Obs Tempos Verbais'] = ""

# Avaliar cada serviço nas colunas especificadas
for idx, row in df_entrada.iterrows():
    pontuacoes = []
    observacoes_gerais = []

    for coluna in colunas_para_avaliar:
        if pd.notnull(row[coluna]):
            texto_coluna = str(row[coluna])
            pontuacao, observacoes = avaliar_tempo_verbal_pessoa(texto_coluna)
            pontuacoes.append(pontuacao)
            if observacoes:
                observacoes_gerais.append(f"{coluna}: {', '.join(observacoes)}")

    # Calcular a média das pontuações
    media_pontuacao = calcular_media_pontuacoes(pontuacoes)

    # Atualizar a coluna de notas e observações no arquivo de saída
    df_saida.at[idx, 'Nota Tempos Verbais'] = media_pontuacao
    df_saida.at[idx, 'Obs Tempos Verbais'] = "; ".join(observacoes_gerais) if observacoes_gerais else "Todos os critérios atendidos"

# Salvar o arquivo atualizado
df_saida.to_excel('RankingCarta.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
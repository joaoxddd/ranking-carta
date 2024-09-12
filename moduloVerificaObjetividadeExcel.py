import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Função para calcular a pontuação do título
def calcular_pontuacao_titulo(titulo):
    if not titulo.strip():
        return 0

    doc = nlp(titulo)
    palavras = [token.text for token in doc]
    pontuacao = 0

    # Verificar se a primeira palavra é um verbo
    if doc[0].pos_ == "VERB":
        pontuacao += 2  # Pontuação por iniciar com verbo

    # Verificar se o verbo está no infinitivo
    for token in doc:
        if token.pos_ == "VERB" and token.morph.get("VerbForm") == ["Inf"]:
            pontuacao += 1.5  # Pontuação por verbo no infinitivo
            break

    # Verificar se o título tem entre 3 e 5 palavras
    if 3 <= len(palavras) <= 5:
        pontuacao += 1.5  # Pontuação por título entre 3 e 5 palavras

    return pontuacao

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx')

# Converter a coluna de notas para float, caso ainda não esteja
df_saida['Nota moduloVerificaObjetividade.py'] = df_saida['Nota moduloVerificaObjetividade.py'].astype(float)

# Avaliar cada título na coluna "Nome curto"
for idx, row in df_entrada.iterrows():
    if pd.notnull(row["Nome curto"]):
        nota = calcular_pontuacao_titulo(str(row["Nome curto"]))
        df_saida.at[idx, 'Nota moduloVerificaObjetividade.py'] = nota

# Salvar o arquivo atualizado
df_saida.to_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
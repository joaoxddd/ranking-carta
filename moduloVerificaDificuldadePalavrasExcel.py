import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Lista de palavras relacionadas ao consumo de serviços online que não penalizam a nota
palavras_excecao = [
    "access", "sign", "login", "logout", "click", "select", "continue", "proceed",
    "verify", "download", "submit", "review", "confirm", "attach", "upload",
    "create", "register", "choose", "complete"
]

# Função para calcular a pontuação de facilidade de leitura
def calcular_pontuacao_facilidade(texto):
    if not texto.strip():
        return 0

    doc = nlp(texto.lower())  # Convertendo o texto para lowercase
    palavras_faceis = [token.text for token in doc if len(token.text) <= 8 and token.text not in palavras_excecao]
    palavras_medias = [token.text for token in doc if 8 < len(token.text) <= 12 and token.text not in palavras_excecao]
    palavras_dificeis = [token.text for token in doc if len(token.text) > 12 and token.text not in palavras_excecao]
    total_palavras = len(doc)

    if total_palavras == 0:
        return 0

    # Fórmula para calcular a pontuação
    pontuacao = ((len(palavras_faceis) - len(palavras_medias) * 0.2 - len(palavras_dificeis)) / total_palavras) * 5

    # Se a pontuação tende a zero (menor que 0.1), retorna 0
    if pontuacao < 0.1:
        return 0
    else:
        return max(pontuacao, 0)

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx')

# Converter a coluna de notas para float, caso ainda não esteja
df_saida['Nota moduloVerificaDificuldadePalavras.py'] = df_saida['Nota moduloVerificaDificuldadePalavras.py'].astype(float)

# Avaliar cada coluna relevante e somar as notas
for idx, row in df_entrada.iterrows():
    nota_total = 0
    for coluna in ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]:
        if pd.notnull(row[coluna]):
            nota = calcular_pontuacao_facilidade(str(row[coluna]))
            nota_total += nota

    # Atualizar a coluna de notas no arquivo de saída
    df_saida.at[idx, 'Nota moduloVerificaDificuldadePalavras.py'] = nota_total

# Salvar o arquivo atualizado
df_saida.to_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
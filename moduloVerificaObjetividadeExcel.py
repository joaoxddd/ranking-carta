import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_lg")

# Função para calcular a pontuação do título com observações, incluindo critérios não atendidos
def calcular_pontuacao_titulo(titulo):
    if not titulo.strip():
        return 0, "Título vazio"

    # Converter o título para letras minúsculas
    titulo = titulo.lower()

    doc = nlp(titulo)
    palavras = [token.text for token in doc]
    pontuacao = 0
    observacoes = []

    # Verificar se a primeira palavra é um verbo
    if doc[0].pos_ == "VERB":
        pontuacao += 2  # Pontuação por iniciar com verbo
        observacoes.append(f"Inicia com verbo (nota: 2)")
    else:
        observacoes.append(f"Não inicia com verbo (nota: 0)")

    # Verificar se o verbo está no infinitivo
    verbo_infinitivo = False
    for token in doc:
        if token.pos_ == "VERB" and token.morph.get("VerbForm") == ["Inf"]:
            pontuacao += 1.5  # Pontuação por verbo no infinitivo
            observacoes.append(f"Verbo no infinitivo (nota: 1.5)")
            verbo_infinitivo = True
            break
    if not verbo_infinitivo:
        observacoes.append(f"Sem verbo no infinitivo (nota: 0)")

    # Verificar se o título tem entre 3 e 5 palavras
    if 3 <= len(palavras) <= 5:
        pontuacao += 1.5  # Pontuação por título entre 3 e 5 palavras
        observacoes.append(f"Título entre 3 e 5 palavras (nota: 1.5)")
    else:
        observacoes.append(f"Título fora da faixa de 3 a 5 palavras (nota: 0)")

    return pontuacao, "; ".join(observacoes)

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RankingCarta.xlsx')

# Converter a coluna de notas para float, caso ainda não esteja
df_saida['Nota Objetividade'] = df_saida['Nota Objetividade'].astype(float)
df_saida['Obs Objetividade'] = ""  # Inicializar a coluna de observações

# Avaliar cada título na coluna "Nome curto"
for idx, row in df_entrada.iterrows():
    if pd.notnull(row["Nome curto"]):
        # Calcular a nota e as observações com o título em letras minúsculas
        nota, observacao = calcular_pontuacao_titulo(str(row["Nome curto"]))
        df_saida.at[idx, 'Nota Objetividade'] = nota
        df_saida.at[idx, 'Obs Objetividade'] = observacao

# Salvar o arquivo atualizado
df_saida.to_excel('RankingCarta.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
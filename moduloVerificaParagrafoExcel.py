import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_lg")

# Função para contar as frases em um parágrafo
def contar_frases(paragrafo):
    doc = nlp(paragrafo)
    frases = list(doc.sents)  # Obtém as sentenças do parágrafo
    return len(frases)

# Função para calcular a pontuação de acordo com a quantidade de frases por parágrafo
def calcular_pontuacao_paragrafos(texto, campo):
    if not texto.strip():
        return 0, f"{campo}: texto vazio"

    # Tratamento especial: separa o texto em "parágrafos" a cada ponto-e-vírgula
    paragrafos = texto.split(';')  # Divide o texto por ponto-e-vírgula
    pontuacoes = []
    observacoes = []

    for i, paragrafo in enumerate(paragrafos):
        if paragrafo.strip():  # Ignorar parágrafos vazios
            numero_frases = contar_frases(paragrafo)

            # Atribuir nota de acordo com o número de frases
            if 1 <= numero_frases <= 3:
                pontuacao = 5
                observacoes.append(f"{campo}: parágrafo {i+1} com 1 a 3 frases (nota: {pontuacao})")
            elif 4 <= numero_frases <= 6:
                pontuacao = 2.5
                observacoes.append(f"{campo}: parágrafo {i+1} com 4 a 6 frases (nota: {pontuacao})")
            else:
                pontuacao = 0  # Mais de 6 frases
                observacoes.append(f"{campo}: parágrafo {i+1} com mais de 6 frases (nota: {pontuacao})")

            pontuacoes.append(pontuacao)

    # Retorna a média das notas dos parágrafos e as observações
    if len(pontuacoes) == 0:
        return 0, f"{campo}: sem parágrafos válidos"
    else:
        media_pontuacao = sum(pontuacoes) / len(pontuacoes)
        return media_pontuacao, "; ".join(observacoes)

# Função para calcular a pontuação final com base na média
def calcular_pontuacao_final(pontuacoes):
    if not pontuacoes:
        return 0  # Nenhuma pontuação para avaliar

    # Cálculo correto da média da pontuação
    media_pontuacao = sum(pontuacoes) / len(pontuacoes)
    return media_pontuacao

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RankingCarta.xlsx')

# Inicializar as colunas de notas e observações
df_saida['Nota Paragrafos'] = 0.0
df_saida['Obs Paragrafos'] = ""  # Inicializar a coluna de observações

# Avaliar cada coluna relevante e calcular a média das notas
for idx, row in df_entrada.iterrows():
    pontuacoes = []
    observacoes_gerais = []

    # Avaliar os campos específicos
    for coluna in ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]:
        if pd.notnull(row[coluna]):  # Ignorar campos nulos
            nota, observacao = calcular_pontuacao_paragrafos(str(row[coluna]), coluna)
            pontuacoes.append(nota)

            # Adicionar observação para todos os parágrafos
            if observacao:
                observacoes_gerais.append(observacao)

    # Calcular a média das notas de todos os campos avaliados
    if pontuacoes:
        pontuacao_final = calcular_pontuacao_final(pontuacoes)
    else:
        pontuacao_final = 0  # Se não houver pontuações, definir como 0

    # Atualizar a coluna de notas e de observações no arquivo de saída
    df_saida.at[idx, 'Nota Paragrafos'] = pontuacao_final
    df_saida.at[idx, 'Obs Paragrafos'] = "; ".join(observacoes_gerais)  # Concatenar as observações

# Salvar o arquivo atualizado
df_saida.to_excel('RankingCarta.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
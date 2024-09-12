import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Função para contar as frases em um parágrafo
def contar_frases(paragrafo):
    doc = nlp(paragrafo)
    frases = list(doc.sents)  # Obtém as sentenças do parágrafo
    return len(frases)

# Função para calcular a pontuação de acordo com a quantidade de frases por parágrafo
def calcular_pontuacao_paragrafos(texto):
    if not texto.strip():
        return 0
    
    # Tratamento especial: separa o texto em "parágrafos" a cada ponto-e-vírgula
    paragrafos = texto.split(';')  # Divide o texto por ponto-e-vírgula
    pontuacao_total = 0
    paragrafos_validos = 0
    
    for paragrafo in paragrafos:
        if paragrafo.strip():  # Ignorar parágrafos vazios
            numero_frases = contar_frases(paragrafo)
            
            # Atribuir nota de acordo com o número de frases
            if 1 <= numero_frases <= 3:
                pontuacao_total += 5
            elif 4 <= numero_frases <= 6:
                pontuacao_total += 2.5
            else:
                pontuacao_total += 0  # Mais de 6 frases

            paragrafos_validos += 1

    # Retorna a média das notas dos parágrafos
    if paragrafos_validos == 0:
        return 0
    else:
        return pontuacao_total / paragrafos_validos

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx')

# Converter a coluna de notas para float, caso ainda não esteja
df_saida['Nota moduloVerificaParagrafo.py'] = df_saida['Nota moduloVerificaParagrafo.py'].astype(float)

# Avaliar cada coluna relevante e somar as notas
for idx, row in df_entrada.iterrows():
    nota_total = 0
    for coluna in ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]:
        if pd.notnull(row[coluna]):
            nota = calcular_pontuacao_paragrafos(str(row[coluna]))
            nota_total += nota

    # Atualizar a coluna de notas no arquivo de saída
    df_saida.at[idx, 'Nota moduloVerificaParagrafo.py'] = nota_total

# Salvar o arquivo atualizado
df_saida.to_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
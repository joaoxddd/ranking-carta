import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Função para avaliar caracteres especiais em um texto
def avaliar_caracteres_especiais(texto):
    if not texto.strip():  # Se o texto está vazio, retorna 0
        return 0
    
    # Remover espaços em branco no início e fim do texto
    texto = texto.strip()
    
    # Definir os caracteres especiais como qualquer coisa que não seja alfanumérica ou espaço
    caracteres_especiais = sum(1 for char in texto if not char.isalnum() and not char.isspace())
    
    # Avaliar a nota conforme a quantidade de caracteres especiais
    if caracteres_especiais == 0:
        return 5
    elif caracteres_especiais <= 2:
        return 4
    elif caracteres_especiais <= 4:
        return 3
    elif caracteres_especiais <= 6:
        return 2
    elif caracteres_especiais <= 8:
        return 1
    else:
        return 0

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx')

# Converter a coluna de notas para float, caso ainda não esteja
df_saida['Nota moduloVerificaCaracteresEspeciais.py'] = df_saida['Nota moduloVerificaCaracteresEspeciais.py'].astype(float)

# Avaliar cada coluna relevante e somar as notas
for idx, row in df_entrada.iterrows():
    nota_total = 0
    for coluna in ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]:
        if pd.notnull(row[coluna]):
            nota = avaliar_caracteres_especiais(str(row[coluna]))
            nota_total += nota

    # Atualizar a coluna de notas no arquivo de saída
    df_saida.at[idx, 'Nota moduloVerificaCaracteresEspeciais.py'] = nota_total

# Salvar o arquivo atualizado
df_saida.to_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
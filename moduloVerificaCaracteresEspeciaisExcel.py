import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_lg")

# Conjunto para armazenar caracteres especiais detectados
caracteres_especiais_detectados = set()

# Função para avaliar caracteres especiais em um texto
def avaliar_caracteres_especiais(texto):
    if not texto.strip():  # Se o texto está vazio, retorna 0
        return 0, []

    # Remover espaços em branco no início e fim do texto
    texto = texto.strip()
    
    # Definir os caracteres especiais como qualquer coisa que não seja alfanumérica, espaço ou ':'
    caracteres_especiais = [char for char in texto if not char.isalnum() and not char.isspace() and char != ':']
    
    # Adicionar os caracteres especiais ao conjunto
    caracteres_especiais_detectados.update(caracteres_especiais)

    # Avaliar a nota conforme a quantidade de caracteres especiais
    qtd_caracteres_especiais = len(caracteres_especiais)
    
    if qtd_caracteres_especiais == 0:
        return 5, caracteres_especiais
    elif qtd_caracteres_especiais <= 2:
        return 4, caracteres_especiais
    elif qtd_caracteres_especiais <= 4:
        return 3, caracteres_especiais
    elif qtd_caracteres_especiais <= 6:
        return 2, caracteres_especiais
    elif qtd_caracteres_especiais <= 8:
        return 1, caracteres_especiais
    else:
        return 0, caracteres_especiais

# Função para calcular a pontuação final com base na média das notas
def calcular_pontuacao_final(pontuacoes):
    if not pontuacoes:
        return 0  # Nenhuma pontuação para avaliar

    media_pontuacao = sum(pontuacoes) / len(pontuacoes)
    return max(min(media_pontuacao, 5), 0)  # Garantir que o valor esteja no intervalo de 0 a 5

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RankingCarta.xlsx')

# Inicializar a coluna de observações
df_saida['Obs Caracteres Especiais'] = ""

# Avaliar cada coluna relevante e calcular a média das notas
for idx, row in df_entrada.iterrows():
    pontuacoes = []
    observacoes_gerais = []

    for coluna in ["Nome do serviço", "Nome curto"]:
        if pd.notnull(row[coluna]):
            texto_coluna = str(row[coluna]).lower()  # Convertendo o texto da coluna para minúsculas
            nota, caracteres_encontrados = avaliar_caracteres_especiais(texto_coluna)
            pontuacoes.append(nota)
            if caracteres_encontrados:
                observacoes_gerais.append(f"{coluna}: Caracteres especiais encontrados: {caracteres_encontrados}")

    # Calcular a pontuação final com base na média das pontuações
    pontuacao_final = calcular_pontuacao_final(pontuacoes)

    # Atualizar a coluna de notas e observações no arquivo de saída
    df_saida.at[idx, 'Nota Caracteres Especiais'] = pontuacao_final
    df_saida.at[idx, 'Obs Caracteres Especiais'] = "; ".join(observacoes_gerais) if observacoes_gerais else ""

# Salvar o arquivo atualizado
df_saida.to_excel('RankingCarta.xlsx', index=False)

# Exibir caracteres especiais encontrados
print("\nCaracteres Especiais Detectados:")
print(sorted(caracteres_especiais_detectados))

print("\nArquivo atualizado com sucesso!")
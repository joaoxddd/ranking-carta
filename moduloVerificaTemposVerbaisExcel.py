import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Função para avaliar tempos verbais
def avaliar_tempo_verbal_pessoa(texto):
    doc = nlp(texto)
    pontuacao = 0

    for token in doc:
        if token.pos_ == "VERB":  # Verificar apenas verbos
            pessoa = token.morph.get("Person")  # Identificar a pessoa do verbo (1, 2 ou 3)
            numero = token.morph.get("Number")  # Identificar o número (Singular/Plural)
            modo = token.morph.get("Mood")  # Identificar o modo do verbo (Imperativo, Indicativo, etc.)
            verbo_forma = token.morph.get("VerbForm")  # Identificar se o verbo está no infinitivo

            # Verifica se pessoa não foi detectada e tenta inferir pelo contexto
            if not pessoa:
                if token.text.lower().endswith(("s", "mos", "m")):
                    pessoa = ["1"]
                elif token.text.lower().endswith(("a", "e", "ou")):
                    pessoa = ["3"]
                elif token.text.lower().endswith(("a", "e")) and token.text.lower() != "se":
                    pessoa = ["2"]

            # Atribuição de pontuação conforme as regras:
            if pessoa == ["2"] and numero == ["Sing"]:
                pontuacao = 5
            elif pessoa == ["3"] and numero == ["Sing"]:
                pontuacao = 5
            elif pessoa == ["2"] and numero == ["Plur"]:
                pontuacao = 3
            elif pessoa == ["3"] and numero == ["Plur"]:
                pontuacao = 3
            elif pessoa == ["1"] and numero == ["Sing"]:
                pontuacao = 1.5
            elif pessoa == ["1"] and numero == ["Plur"]:
                pontuacao = 0
            # Se não há pessoa explícita, mas o verbo está no imperativo
            elif not pessoa and modo == ["Imp"]:
                if numero == ["Sing"]:
                    pontuacao = 5  # Sujeito implícito na 2ª pessoa do singular
                elif numero == ["Plur"]:
                    pontuacao = 3  # Sujeito implícito na 2ª pessoa do plural

            # Verifica se o verbo está no infinitivo (frequente em instruções)
            elif verbo_forma == ["Inf"]:
                pontuacao = 5  # Considera como instrução

            # Retorna após o primeiro verbo relevante encontrado
            return pontuacao

    # Retorna 0 se não houver verbo relevante encontrado
    return pontuacao

# Carregar os arquivos
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx')

# Colunas para serem analisadas
colunas_para_avaliar = ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]

# Convertendo a coluna para float para aceitar valores decimais
df_saida['Nota moduloVerificaTemposVerbais.py'] = df_saida['Nota moduloVerificaTemposVerbais.py'].astype(float)

# Avaliar cada serviço nas colunas especificadas
for idx, row in df_entrada.iterrows():
    nota_total = 0
    for coluna in colunas_para_avaliar:
        if pd.notnull(row[coluna]):
            nota_total += avaliar_tempo_verbal_pessoa(str(row[coluna]))

    # Atualizar a coluna de saída correspondente ao índice
    df_saida.at[idx, 'Nota moduloVerificaTemposVerbais.py'] = nota_total

# Salvar o arquivo atualizado
df_saida.to_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
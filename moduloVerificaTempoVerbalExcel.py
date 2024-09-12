import spacy
import pandas as pd

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Função para verificar se o verbo auxiliar está no presente
def verbo_aux_presente(token):
    return token.dep_ == "aux" and token.head.morph.get("Tense") == ["Pres"]

# Função para verificar manualmente se o verbo está no futuro
def detectar_futuro(token):
    return token.text.endswith("rei") or token.text.endswith("rá") or token.text.endswith("rão")

# Função para avaliar o uso de verbos no presente em uma única frase
def avaliar_tempo_verbal_frase(frase):
    doc = nlp(frase)  # Processa a frase com Spacy
    verbo_presente = False
    verbo_outros_tempos = False

    for token in doc:
        if token.pos_ == "VERB":  # Se for um verbo
            eh_futuro = detectar_futuro(token)
            tempo_verbal = token.morph.get("Tense")
            
            # Verificação manual para verbos no presente e futuro
            if tempo_verbal == ["Pres"] or verbo_aux_presente(token) or "ndo" in token.text:
                verbo_presente = True
            elif eh_futuro or tempo_verbal == ["Fut"]:
                verbo_outros_tempos = True

    # Avaliar a nota conforme os critérios
    if verbo_presente and not verbo_outros_tempos:
        return 5  # Somente verbos no presente
    elif verbo_presente and verbo_outros_tempos:
        return 2.5  # Verbos no presente e outros tempos
    elif verbo_outros_tempos:
        return 0  # Verbos em outro tempo, mas não no presente
    else:
        return 0  # Nenhum verbo relevante encontrado

# Função principal para avaliar o uso de verbos no presente em um texto com múltiplas frases
def avaliar_tempo_verbal(texto):
    if not texto.strip():
        return 0
    
    doc = nlp(texto)
    nota_total = 0
    frase_count = 0

    for frase in doc.sents:
        nota_frase = avaliar_tempo_verbal_frase(frase.text)
        nota_total += nota_frase
        frase_count += 1

    return nota_total / frase_count if frase_count > 0 else 0

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx')

# Converter a coluna de notas para float, caso ainda não esteja
df_saida['Nota moduloVerificaTempoVerbal.py'] = df_saida['Nota moduloVerificaTempoVerbal.py'].astype(float)

# Avaliar cada coluna relevante e somar as notas
for idx, row in df_entrada.iterrows():
    nota_total = 0
    for coluna in ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]:
        if pd.notnull(row[coluna]):
            nota = avaliar_tempo_verbal(str(row[coluna]))
            nota_total += nota

    # Atualizar a coluna de notas no arquivo de saída
    df_saida.at[idx, 'Nota moduloVerificaTempoVerbal.py'] = nota_total

# Salvar o arquivo atualizado
df_saida.to_excel('RelatorioServicosCarta10-09-24_atualizado_acrescentando_colunas_notas.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
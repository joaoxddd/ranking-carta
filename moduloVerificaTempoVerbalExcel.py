import spacy
import pandas as pd
import re

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_lg")

# Expressão regular para detectar URLs
url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

# Função para verificar se o verbo auxiliar está no presente
def verbo_aux_presente(token):
    return token.dep_ == "aux" and token.head.morph.get("Tense") == ["Pres"]

# Função para verificar manualmente se o verbo está no futuro
def detectar_futuro(token):
    return token.text.endswith("rei") or token.text.endswith("rá") or token.text.endswith("rão")

# Função para verificar se o verbo está no infinitivo
def verbo_infinitivo_como_presente(token):
    return token.morph.get("VerbForm") == ["Inf"]

# Função para verificar se o verbo está no particípio passado (que não deve ser contado como verbo)
def verbo_participio_passado(token):
    return token.morph.get("VerbForm") == ["Part"]

# Função para verificar se o verbo está no gerúndio
def verbo_gerundio(token):
    return token.morph.get("VerbForm") == ["Ger"]

# Função para verificar se o verbo está no modo imperativo
def verbo_imperativo(token):
    return token.morph.get("Mood") == ["Imp"]

# Função para remover URLs do texto
def remover_urls(texto):
    return url_pattern.sub('', texto)

# Função para avaliar o uso de verbos no presente, infinitivo, gerúndio ou imperativo em uma única frase
# Verbo no particípio passado não será considerado como verbo
def avaliar_tempo_verbal_frase(frase):
    frase_sem_url = remover_urls(frase.lower())  # Remover URLs e converter texto para minúsculas
    doc = nlp(frase_sem_url)  # Processa a frase com Spacy
    verbo_presente = False
    verbo_outros_tempos = False
    observacoes = []
    verbos_identificados = False  # Verifica se algum verbo foi identificado

    for token in doc:
        if token.pos_ == "VERB" and not verbo_participio_passado(token):  # Ignorar verbos no particípio passado
            verbos_identificados = True  # Um verbo foi identificado
            verbo = f"[{token.text}]"  # Colocar o verbo entre colchetes
            eh_futuro = detectar_futuro(token)
            tempo_verbal = token.morph.get("Tense")
            
            # Verificação para verbos no presente, infinitivo, gerúndio ou imperativo
            if verbo_imperativo(token):  # Verbo no modo imperativo
                verbo_presente = True
                observacoes.append(f"Verbo no imperativo {verbo} (nota: 5)")
            elif tempo_verbal == ["Pres"]:
                verbo_presente = True
                observacoes.append(f"Verbo no presente {verbo} (nota: 5)")
            elif verbo_aux_presente(token):
                verbo_presente = True
                observacoes.append(f"Verbo auxiliar no presente {verbo} (nota: 5)")
            elif verbo_infinitivo_como_presente(token):
                verbo_presente = True
                observacoes.append(f"Verbo no infinitivo {verbo} (nota: 5)")
            elif verbo_gerundio(token):
                verbo_presente = True
                observacoes.append(f"Verbo no gerúndio {verbo} (nota: 5)")
            elif eh_futuro:
                verbo_outros_tempos = True
                observacoes.append(f"Verbo no futuro {verbo} (nota: 0)")
            else:
                verbo_outros_tempos = True
                observacoes.append(f"Verbo em outro tempo {verbo} (nota: 0)")

    # Caso nenhum verbo (exceto particípio passado) seja identificado
    if not verbos_identificados:
        observacoes.append("Nenhum verbo foi identificado (nota: 0)")

    # Avaliar a nota conforme os critérios
    if verbo_presente and not verbo_outros_tempos:
        return 5, "; ".join(observacoes)  # Somente verbos no presente, infinitivo, gerúndio ou imperativo
    elif verbo_presente and verbo_outros_tempos:
        return 2.5, "; ".join(observacoes)  # Verbos no presente (ou equivalentes) e outros tempos
    else:
        return 0, "; ".join(observacoes)  # Nenhum verbo no presente ou equivalentes encontrado

# Função principal para avaliar o uso de verbos no presente ou equivalentes em um texto com múltiplas frases
def avaliar_tempo_verbal(texto):
    if not texto.strip():
        return 0, "Texto vazio"
    
    doc = nlp(remover_urls(texto.lower()))  # Remover URLs e converter texto para minúsculas
    pontuacoes = []
    observacoes_gerais = []

    for frase in doc.sents:
        nota_frase, observacao = avaliar_tempo_verbal_frase(frase.text)
        pontuacoes.append(nota_frase)
        observacoes_gerais.append(observacao)

    # Retornar a pontuação mais baixa encontrada (mais restritiva) e observações
    return (min(pontuacoes) if pontuacoes else 0), "; ".join(observacoes_gerais)

# Função para calcular a média das pontuações obtidas por vários campos
def calcular_media_pontuacoes(pontuacoes):
    if not pontuacoes:
        return 0
    return sum(pontuacoes) / len(pontuacoes)

# Carregar os arquivos de entrada e saída
df_entrada = pd.read_excel('RelatorioSemColunas.xlsx')
df_saida = pd.read_excel('RankingCarta.xlsx')

# Converter a coluna de notas para float, caso ainda não esteja
df_saida['Nota Tempo Verbal'] = df_saida['Nota Tempo Verbal'].astype(float)
df_saida['Obs Tempo Verbal'] = ""  # Inicializar a coluna de observações

# Avaliar cada coluna relevante e calcular a média das notas
for idx, row in df_entrada.iterrows():
    pontuacoes = []
    observacoes_gerais = []

    for coluna in ["Nome do serviço", "Nome curto", "Como solicitar online", "Como solicitar presencial", "Como solicitar telefonico"]:
        if pd.notnull(row[coluna]):
            nota, observacao = avaliar_tempo_verbal(str(row[coluna]))
            pontuacoes.append(nota)
            observacoes_gerais.append(f"{coluna}: {observacao}")

    # Calcular a média das pontuações
    media_pontuacao = calcular_media_pontuacoes(pontuacoes)

    # Atualizar a coluna de notas e de observações no arquivo de saída
    df_saida.at[idx, 'Nota Tempo Verbal'] = media_pontuacao
    df_saida.at[idx, 'Obs Tempo Verbal'] = "; ".join(observacoes_gerais)

# Salvar o arquivo atualizado
df_saida.to_excel('RankingCarta.xlsx', index=False)

print("Arquivo atualizado com sucesso!")
import spacy

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

# Teste
# Verificar se o título tem entre 3 e 5 palavra
exemplo_1 = "Fazer a inscrição online"
exemplo_2 = "Baixar o relatório financeiro"
exemplo_3 = "Cadastrar-se no sistema"
exemplo_4 = "Fazendo seu cadastro no sistema da SEFAZ"
exemplo_5 = "SEFAZ - seu cadastro no sistema da SEFAZ"

print(f"Pontuação do título '{exemplo_1}': {calcular_pontuacao_titulo(exemplo_1)}")
print(f"Pontuação do título '{exemplo_2}': {calcular_pontuacao_titulo(exemplo_2)}")
print(f"Pontuação do título '{exemplo_3}': {calcular_pontuacao_titulo(exemplo_3)}")
print(f"Pontuação do título '{exemplo_4}': {calcular_pontuacao_titulo(exemplo_4)}")
print(f"Pontuação do título '{exemplo_5}': {calcular_pontuacao_titulo(exemplo_5)}")
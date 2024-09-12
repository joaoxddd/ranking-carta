import spacy

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Função para verificar se uma frase indica uma única ação
def unica_acao(frase):
    doc = nlp(frase)
    
    # Verificar se há mais de um verbo principal (ROOT)
    verbos_raiz = [token for token in doc if token.dep_ == "ROOT" and token.pos_ == "VERB"]
    
    conj_apos_verbo = False
    for token in doc:
        if token.pos_ == "CCONJ":  # Se for uma conjunção coordenativa
            next_token = token.nbor(1) if token.i + 1 < len(doc) else None
            if next_token and next_token.pos_ == "VERB":
                # Verificar se os verbos estão conectados por uma relação de dependência
                if next_token.head != token.head:
                    conj_apos_verbo = True
                    break

    return len(verbos_raiz) == 1 and not conj_apos_verbo

# Função para verificar se a frase está na forma direta (verbo no início)
def forma_direta(frase):
    doc = nlp(frase)
    if len(doc) > 0 and doc[0].pos_ == "VERB":  # Verifica se a primeira palavra é um verbo
        return True
    return False

# Função para calcular a pontuação com base nos critérios fornecidos
def avaliar_frase(frase):
    doc = nlp(frase)
    pontuacao = 0
    
    # Critério 1: Frases com no máximo 10 palavras
    if len(doc) <= 10:
        pontuacao += 2
    else:
        pontuacao += 0

    # Critério 2: Frase indica uma única ação
    if unica_acao(frase):
        pontuacao += 1
    else:
        pontuacao += 0

    # Critério 3: Frase na forma direta (verbo no início)
    if forma_direta(frase):
        pontuacao += 1
    else:
        pontuacao += 0
    
    return pontuacao

# Teste
frase_1 = "Faça seu cadastro no site."  # Frase curta, uma ação, forma direta. 4 pontos
frase_2 = "Você deve fazer seu cadastro no mercado e depois se cadastrar novamente."  # Mais de uma ação
frase_3 = "Complete o formulário para seguir adiante. E depois de seguir, faça um segundo cadastro."  # Forma direta
frase_4 = "Complete o formulário e verifique as informações para enviar."  # Mais de uma ação, menos de 10 palavras

print(f"Pontuação frase 1: {avaliar_frase(frase_1)}")
print(f"Pontuação frase 2: {avaliar_frase(frase_2)}")
print(f"Pontuação frase 3: {avaliar_frase(frase_3)}")
print(f"Pontuação frase 4: {avaliar_frase(frase_4)}")
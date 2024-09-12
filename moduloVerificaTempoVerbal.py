import spacy

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Função para verificar se o verbo auxiliar está no presente
def verbo_aux_presente(token):
    return token.dep_ == "aux" and token.head.morph.get("Tense") == ["Pres"]

# Função para verificar manualmente se o verbo está no futuro
def detectar_futuro(token):
    # Verifica se o verbo termina com "rei", "rá", "rão", que são típicas terminações do futuro
    return token.text.endswith("rei") or token.text.endswith("rá") or token.text.endswith("rão")

# Função para avaliar o uso de verbos no presente em uma única frase
def avaliar_tempo_verbal_frase(frase):
    doc = nlp(frase)  # Processa a frase com Spacy
    verbo_presente = False
    verbo_outros_tempos = False

    for token in doc:
        if token.pos_ == "VERB":  # Se for um verbo
            # Verificar o tempo verbal manualmente para futuro
            eh_futuro = detectar_futuro(token)
            tempo_verbal = token.morph.get("Tense")
            
            print(f"Verbo encontrado: {token.text}, Lema: {token.lemma_}, Tempo Verbal: {tempo_verbal}, Futuro Manual: {eh_futuro}")
            
            # Verificação manual para verbos no presente e futuro
            if tempo_verbal == ["Pres"] or verbo_aux_presente(token) or "ndo" in token.text:
                verbo_presente = True
            elif eh_futuro or tempo_verbal == ["Fut"]:  # Prioriza o futuro detectado manualmente
                verbo_outros_tempos = True

    # Avaliar a nota conforme os critérios
    if verbo_presente and not verbo_outros_tempos:
        return 5  # Somente verbos no presente
    elif verbo_presente and verbo_outros_tempos:
        return 2.5  # Verbos no presente e outros tempos (futuro, passado)
    elif verbo_outros_tempos:  # Se for apenas futuro ou outro tempo
        return 0  # Não há verbos no presente, mas outros tempos verbais
    else:
        return 0  # Nenhum verbo relevante encontrado

# Função principal para avaliar o uso de verbos no presente em um texto com múltiplas frases
def avaliar_tempo_verbal(texto):
    if not texto.strip():  # Verifica se o texto está vazio
        return 0
    
    doc = nlp(texto)  # Processa o texto usando Spacy
    nota_total = 0
    frase_count = 0

    # Processa cada frase separadamente
    for frase in doc.sents:
        print(f"\nProcessando frase: {frase.text}")
        nota_frase = avaliar_tempo_verbal_frase(frase.text)
        print(f"Nota para a frase: {nota_frase}")
        nota_total += nota_frase
        frase_count += 1

    # Retorna a média das notas das frases
    nota_media = nota_total / frase_count if frase_count > 0 else 0
    print(f"Nota média para o texto: {nota_media}")
    return nota_media

# Teste com exemplos
exemplo_1 = "Indicar um lugar para interagir."  # Deve retornar 0
exemplo_2 = "Esteja conforme a localidade e indique em algum lugar."  # Deve retornar 5
exemplo_3 = "Indique um lugar para interagir."  # Deve retornar 5
exemplo_4 = "Indique um lugar para interagir. Interagir conforme necessario."  # Deve retornar 5

avaliar_tempo_verbal(exemplo_1)
avaliar_tempo_verbal(exemplo_2)
avaliar_tempo_verbal(exemplo_3)
avaliar_tempo_verbal(exemplo_4)
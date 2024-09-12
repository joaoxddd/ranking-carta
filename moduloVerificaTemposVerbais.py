import spacy

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

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

# Teste
frase_1 = "Você vai ao mercado."  # 2ª pessoa do singular
frase_2 = "Nós vamos ao mercado."  # 1ª pessoa do plural
frase_3 = "Os contribuintes estudam para o vestibular e para passarem em um concurso."  # 3ª pessoa do plural
frase_4 = "Tu estás estudando para qual curso?"  # 2ª pessoa do singular
frase_5 = "O cliente acessa a Sala do Cliente no site da CEGÁS (http://saladocliente.cegas.com.br/salacliente/)"
frase_6 = "Acessar o endereço eletrônico: http://sistemas.detran.ce.gov.br/central. Clicar em: Habilitação. Clicar em: Reabilitação. Informar o número do CPF. Informar o número da CNH."
frase_7 = "Insere seu CNPJ e a sua Senha."

print(f"Pontuação frase 1: {avaliar_tempo_verbal_pessoa(frase_1)}")  # 5
print(f"Pontuação frase 2: {avaliar_tempo_verbal_pessoa(frase_2)}")  # 0
print(f"Pontuação frase 3: {avaliar_tempo_verbal_pessoa(frase_3)}")  # 3
print(f"Pontuação frase 4: {avaliar_tempo_verbal_pessoa(frase_4)}")  # 5
print(f"Pontuação frase 5: {avaliar_tempo_verbal_pessoa(frase_5)}")  # 5
print(f"Pontuação frase 6: {avaliar_tempo_verbal_pessoa(frase_6)}")  # 5
print(f"Pontuação frase 7: {avaliar_tempo_verbal_pessoa(frase_7)}")  # 5
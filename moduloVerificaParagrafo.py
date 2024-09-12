import spacy

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
            print(f"Parágrafo: '{paragrafo}'\nNúmero de frases: {numero_frases}")
            
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

# Teste com exemplos
exemplo = "Este é o primeiro parágrafo com uma frase; Este é o segundo parágrafo. Ele contém duas frases; Agora temos um parágrafo mais longo. Ele possui várias frases. Isso pode afetar a pontuação."
print("Pontuação de parágrafos:", calcular_pontuacao_paragrafos(exemplo))

exemplo2 = "O avanço das tecnologias de machine learning e cloud computing tem revolucionado o mercado global. Atualmente, muitas empresas adotam a estratégia de e-commerce, que possibilita a venda de produtos e serviços online com facilidade. No entanto, o aumento do uso de smartphones e dispositivos móveis também traz desafios, como a necessidade de aprimorar os sistemas de cybersecurity. Durante uma conferência sobre big data, diversos profissionais discutira como algoritmos de data mining estão sendo implementados para melhorar a experiência do usuário em plataformas de streaming, como o Netflix e o Spotify. Esses avanços tecnológicos também permitem que se faça upload e download de arquivos em uma velocidade impressionante, revolucionando a forma como consumimos dados. Além disso, as startups estão explorando cada vez mais o conceito de blockchain para criar novos modelos de negócio, o que gera uma grande expectativa no setor financeiro."
print("Pontuação de parágrafos:", calcular_pontuacao_paragrafos(exemplo2))
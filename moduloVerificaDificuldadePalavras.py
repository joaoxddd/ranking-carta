import spacy

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Lista de palavras relacionadas ao consumo de serviços online que não penalizam a nota
palavras_excecao = [
    "access", "sign", "login", "logout", "click", "select", "continue", "proceed",
    "verify", "download", "submit", "review", "confirm", "attach", "upload",
    "create", "register", "choose", "complete"
]

# Função para calcular a pontuação de facilidade de leitura
def calcular_pontuacao_facilidade(texto):
    if not texto.strip():
        return 0

    doc = nlp(texto.lower())  # Convertendo o texto para lowercase
    palavras_faceis = [token.text for token in doc if len(token.text) <= 8 and token.text not in palavras_excecao]
    palavras_medias = [token.text for token in doc if 8 < len(token.text) <= 12 and token.text not in palavras_excecao]
    palavras_dificeis = [token.text for token in doc if len(token.text) > 12 and token.text not in palavras_excecao]
    total_palavras = len(doc)

    if total_palavras == 0:
        return 0

    # Fórmula para calcular a pontuação
    pontuacao = ((len(palavras_faceis) - len(palavras_medias) * 0.2 - len(palavras_dificeis)) / total_palavras) * 5

    # Se a pontuação tende a zero (menor que 0.1), retorna 0
    if pontuacao < 0.1:
        return 0
    else:
        return max(pontuacao, 0)

# Teste
exemplo = "Este é um exemplo simples de texto com palavras fáceis e algumas mais longas."
print("Pontuação de facilidade de leitura:", calcular_pontuacao_facilidade(exemplo))

exemplo2 = "O avanço das tecnologias de machine learning e cloud computing tem revolucionado o mercado global. Atualmente, muitas empresas adotam a estratégia de e-commerce, que possibilita a venda de produtos e serviços online com facilidade. No entanto, o aumento do uso de smartphones e dispositivos móveis também traz desafios, como a necessidade de aprimorar os sistemas de cybersecurity. Durante uma conferência sobre big data, diversos profissionais discutira como algoritmos de data mining estão sendo implementados para melhorar a experiência do usuário em plataformas de streaming, como o Netflix e o Spotify. Esses avanços tecnológicos também permitem que se faça upload e download de arquivos em uma velocidade impressionante, revolucionando a forma como consumimos dados. Além disso, as startups estão explorando cada vez mais o conceito de blockchain para criar novos modelos de negócio, o que gera uma grande expectativa no setor financeiro."
print("Pontuação de facilidade de leitura:", calcular_pontuacao_facilidade(exemplo2))
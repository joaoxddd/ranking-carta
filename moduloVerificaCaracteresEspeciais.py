import spacy
import string

# Carregar o modelo de português do Spacy
nlp = spacy.load("pt_core_news_sm")

# Função para avaliar caracteres especiais em um texto
def avaliar_caracteres_especiais(texto):
    if not texto.strip():  # Se o texto está vazio, retorna 0
        return 0
    
    # Remover espaços em branco no início e fim do texto
    texto = texto.strip()
    
    # Definir os caracteres especiais como qualquer coisa que não seja alfanumérica ou espaço
    caracteres_especiais = sum(1 for char in texto if not char.isalnum() and not char.isspace())
    
    # Avaliar a nota conforme a quantidade de caracteres especiais
    if caracteres_especiais == 0:
        return 5
    elif caracteres_especiais <= 2:
        return 4
    elif caracteres_especiais <= 4:
        return 3
    elif caracteres_especiais <= 6:
        return 2
    elif caracteres_especiais <= 8:
        return 1
    else:
        return 0

# Teste com exemplos
exemplo_1 = "Indique um lugar para interagir."  # Nenhum caractere especial, deve retornar 5
exemplo_2 = "Indique um lugar @para interagir."  # 2 caracteres especiais, deve retornar 4
exemplo_3 = "Indique um lugar @para interagir com * mais caracteres!"  # 4 caracteres especiais, deve retornar 3
exemplo_4 = "Oi."  # 4 caracteres especiais, deve retornar 3

print(avaliar_caracteres_especiais(exemplo_1))
print(avaliar_caracteres_especiais(exemplo_2))
print(avaliar_caracteres_especiais(exemplo_3))
print(avaliar_caracteres_especiais(exemplo_4))
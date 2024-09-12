# ranking-carta

Módulos em Python baseados na biblioteca de NLP spaCy que trata semanticamente e sintaticamente a estrutural textual das entradas. Os módulos são combinados para extrair e avaliar as informações de determinadas base de dados em formato de planilha, onde cada atributo desta planilha é submetido a algum dos módulos de avaliação para, por fim, serem definidas notas de avalição com base nas normas da Abep-tic.

## Índice

- [Recursos](#recursos)
- [Instalação](#instalação)
- [Licença](#licença)

## Recursos

- Avaliação de Texto com base nas regras de negócio definidas pela Abep-tic.
- 7 módulos com exemplos.
- Implementação em python com a utilização de bibliotecas baseadas em NLP.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/joaoxddd/ranking-carta.git
    cd ranking-carta
    ```

2. Instale o python e as bibliotecas necessárias:
   
    ```pip
    pip install -r requirements.txt
    ```
    ```spaCy
    python -m spacy download pt_core_news_sm
    ```
    ```Ativar ambiente do path do virtual env (venv)
    source nome_da_virtualenv/bin/activate
    ```

3. Execute a o Script:

    - Execução do módulo:
    ```bash
    python modulo.py
    ```

## Licença
- Versão 0.0.1

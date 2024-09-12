# ranking-carta

Sistema de inscrições e gerenciamento de turmas e usuários para exportação.

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

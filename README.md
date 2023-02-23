# Akinator like API

API para sistema de adivinhação de pessoas a partir de perguntas e respostas, estilo o site Akinator. O sistema possui um banco de dados com características de 824 pessoas famosas e faz perguntas para tentar adivinhar a pessoa que o usuário pensou.

## Rodando localmente

- Instale as dependênicas com `pip install -r requirements.txt`
- Inicie o servidor com `uvicorn server:app --reload` ou utilize a interface de terminal com `python akinator.py`

## Rotas

A documentação das rotas da API está disponível em https://zcnj6e.deta.dev/docs

## Exemplo de cliente

Exemplo de cliente web que consome essa api

URL: https://rotanika.vercel.app/

Repositório: https://github.com/anapaulaonc/rotanika

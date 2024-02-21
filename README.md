# Akinator like API

API para sistema de adivinhação de pessoas a partir de perguntas e respostas, estilo o site Akinator. O sistema possui um banco de dados com características de 824 pessoas famosas e faz perguntas para tentar adivinhar a pessoa que o usuário pensou.

## API
A API está disponível no endereço https://akinatorapi-1-g4100243.deta.app

## Funcionalidades

- Pode-se responder sim, não ou não sei para as perguntas.
- Indicação da porcetagem de perguntas já feitas e de quantas faltam para a adivinhação.
- Adicionar uma nova pessoa que não está na base de dados junto com uma característica que a diferencie.

## Rodando localmente

- Instale as dependênicas com `pip install -r requirements.txt`
- Inicie o servidor com `uvicorn server:app --reload` ou utilize a interface de terminal com `python akinator.py`

## Rotas

A documentação das rotas da API está disponível em https://akinatorapi-1-g4100243.deta.app/docs

## Demo

Exemplo de cliente web que consome essa api

Site: https://rotanika.vercel.app/

Repositório: https://github.com/anapaulaonc/rotanika

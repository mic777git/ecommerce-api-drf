# E-commerce API

API REST para um sistema de e-commerce simples, construida com Django REST Framework.

## Funcionalidades

- Autenticacao via JWT (access + refresh token)
- Isolamento de dados por usuario (cada usuario so ve seus proprios pedidos)
- Catalogo de produtos organizado por categoria
- Criacao de pedidos com multiplos itens (serializer aninhado)
- Baixa automatica de estoque ao criar um pedido
- Validacao de estoque insuficiente
- Calculo automatico de subtotal por item e total do pedido
- Preco do pedido preservado no momento da compra, mesmo que o preco do produto mude depois

## Stack

- Python / Django
- Django REST Framework
- djangorestframework-simplejwt
- SQLite

## Modelagem

Category (1) para Product (N)
User (1) para Order (N) para OrderItem (N) para Product (1)

## Endpoints

POST /api/token/ - obter access e refresh token
POST /api/token/refresh/ - renovar o access token
GET/POST /api/categories/ - listar ou criar categorias
GET/POST /api/products/ - listar ou criar produtos
GET/POST /api/orders/ - listar pedidos do usuario ou criar novo pedido

## Como rodar localmente

python -m venv venv
venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
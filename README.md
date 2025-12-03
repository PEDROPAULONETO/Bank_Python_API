# Bank Payton API

Bank Payton API é um microsserviço desenvolvido em Python com FastAPI, projetado para gerenciar operações de contas correntes, como criação de contas, depósitos e saques.

## Principais Funcionalidades

- **Autenticação:** Sistema de autenticação seguro baseado em tokens JWT com o fluxo OAuth2.
- **Gerenciamento de Contas:**
  - Criação de novas contas.
  - Listagem de contas por usuário.
- **Gerenciamento de Transações:**
  - Criação de transações (depósito ou saque).
  - Listagem de transações por conta.

## Tecnologias Utilizadas

- **Framework:** FastAPI
- **Banco de Dados:** SQLAlchemy com Alembic para migrações.
- **Validação de Dados:** Pydantic
- **Segurança:** Passlib (para hashing de senhas), python-jose (para JWT), SlowAPI (para rate limiting).
- **Servidor ASGI:** Uvicorn

---
## Melhorias de Segurança Implementadas

A segurança da API foi significativamente aprimorada com as seguintes implementações:

1.  **Hashing Seguro de Senhas:**
    - As senhas dos usuários são hasheadas usando o algoritmo **bcrypt** através da biblioteca `passlib`. Isso previne que senhas sejam armazenadas em texto plano, protegendo-as mesmo em caso de vazamento de dados do banco.

2.  **Autenticação com OAuth2 e JWT:**
    - O sistema de autenticação foi migrado para o fluxo **OAuth2PasswordBearer**, o padrão da indústria para APIs.
    - O login é feito no endpoint `/auth/token`, que retorna um **JSON Web Token (JWT)** com tempo de expiração. Este token deve ser enviado no cabeçalho `Authorization: Bearer <token>` para acessar rotas protegidas.

3.  **Proteção de Endpoints e Autorização:**
    - Todas as rotas de contas e transações agora exigem um token de autenticação válido.
    - O sistema valida não apenas se o usuário está autenticado, mas também se ele é o **dono** do recurso que está tentando acessar (por exemplo, um usuário não pode listar as contas de outro).

4.  **Rate Limiting (Limitação de Requisições):**
    - Para prevenir ataques de força bruta, o endpoint de login (`/auth/token`) foi protegido com um **rate limiter**. Por padrão, ele permite apenas **5 tentativas de login por minuto** a partir do mesmo endereço de IP.

## 🔗 Links
[![github](https://img.shields.io/badge/github-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PEDROPAULONETO/k8s-projeto1-app-base/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedropaulosneto/)

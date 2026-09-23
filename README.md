# API de Cadastro de Personagens

API REST desenvolvida com **FastAPI**, **SQLAlchemy** e **SQLite**, com autenticação via JWT, controle de acesso por usuário/administrador e versionamento de banco de dados com Alembic.

Cada usuário pode cadastrar, visualizar, editar e excluir seus próprios personagens de RPG (mago, guerreiro, lutador, etc.), com atributos individuais (vida, força, sorte, etc.), enquanto administradores têm acesso irrestrito a todos os registros e à gestão de usuários.

## Tecnologias utilizadas

- FastAPI
- SQLAlchemy (ORM)
- Alembic (migrations)
- SQLite
- Passlib (bcrypt) — hash de senhas
- python-jose — geração e validação de tokens JWT
- Pydantic — validação de dados

## Funcionalidades

- Cadastro e login de usuários
- Autenticação via JWT (Bearer Token)
- Login integrado ao Swagger (OAuth2PasswordRequestForm)
- CRUD completo de personagens (criar, listar, visualizar, editar, excluir)
- Sistema de atributos por personagem (vida, escudo, vigor, sorte, inteligência, força), com edição parcial e cálculo automático do total
- Gestão de usuários: promoção e rebaixamento de administradores, exclusão de contas, com proteção contra remoção do último admin do sistema
- Controle de permissão em todas as rotas: cada usuário só acessa seus próprios dados; administradores acessam todos

## Estrutura do projeto

├── main.py                  # Inicialização da aplicação e configurações globais
├── models.py                # Modelos SQLAlchemy (Usuario, Personagem, Atributos)
├── schemas.py                # Schemas Pydantic de entrada/saída
├── dependencies.py            # Sessão de banco e verificação de token JWT
├── auth_routes.py             # Rotas de autenticação e gestão de usuários
├── caracter_routes.py           # Rotas de personagens e atributos
├── seed.py                  # Script para criar o primeiro admin do sistema
└── alembic/                 # Migrations do banco de dados

## Rotas principais

### Autenticação e usuários (/auth)

| Método | Rota | Descrição |
|---|---|---|
| POST | /auth/criar_conta | Cria um novo usuário (sempre não-admin) |
| POST | /auth/login | Login via JSON (email e senha), retorna token JWT |
| POST | /auth/login-form | Login via formulário (usado pelo Swagger) |
| PUT | /auth/promover_admin/{id} | Promove um usuário a administrador (somente admin) |
| PUT | /auth/usuario/rebaixar/{id} | Remove o privilégio de administrador de um usuário (somente admin) |
| POST | /auth/usuario/deletar/{id} | Exclui um usuário — o próprio, ou qualquer um se for admin |

### Personagens (/personagens) — requer autenticação

| Método | Rota | Descrição |
|---|---|---|
| POST | /personagens/personagem | Cria um novo personagem (atributos iniciam zerados) |
| GET | /personagens/ver_personagem/{id} | Visualiza um personagem (dono ou admin) |
| GET | /personagens/listar | Lista todos os personagens do sistema (somente admin) |
| GET | /personagens/listar/personagens-usuario | Lista os personagens do usuário logado |
| PUT | /personagens/editar_personagem/{id} | Edita nome, classe e arma de um personagem (dono ou admin) |
| PUT | /personagens/editar_personaagem/editar_atributos/{id} | Edita os atributos de um personagem — aceita edição parcial |
| POST | /personagens/personagem/excluir/{id} | Exclui um personagem (dono ou admin) |

## Regras de negócio

- Um usuário sempre é criado como não-admin; só um administrador já existente pode promover outro
- O sistema nunca fica sem administrador: rebaixar ou excluir o último admin é bloqueado
- Ao excluir um usuário, seus personagens são excluídos automaticamente (cascade)
- Ao excluir um personagem, seus atributos são excluídos automaticamente (cascade)
- Todo personagem nasce com um conjunto de atributos zerados, criado junto na mesma operação

## Como rodar o projeto localmente

1. Clone o repositório:

git clone <link-do-repositorio>
cd API_cadastro_jogador

2. Crie e ative um ambiente virtual:

python -m venv .venv
.venv\Scripts\activate      # Windows

3. Instale as dependências:

pip install fastapi uvicorn sqlalchemy "passlib[bcrypt]" "python-jose[cryptography]" python-dotenv python-multipart alembic

4. Crie um arquivo .env na raiz do projeto:

SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Rode as migrations para criar as tabelas do banco:

alembic upgrade head

6. Crie o primeiro administrador do sistema:

python seed.py

Esse script cria um admin padrão (email e senha definidos no próprio arquivo) apenas se ainda não existir nenhum administrador no banco. A partir daí, novos admins só podem ser criados promovendo usuários já existentes, pela rota /auth/promover_admin/{id}.

7. Inicie o servidor:

uvicorn main:app --reload

8. Acesse a documentação interativa (Swagger):

http://127.0.0.1:8000/docs

## Testes

Os testes foram realizados manualmente via Swagger, cobrindo os fluxos de cadastro, login, gestão de usuários (promoção, rebaixamento, exclusão) e CRUD de personagens e atributos.

## Próximos passos

- Implementar testes automatizados com pytest e httpx
- Containerizar a aplicação com Docker
- Avaliar a implementação de refresh token
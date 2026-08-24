# API de Cadastro de Personagens

API REST desenvolvida com **FastAPI**, **SQLAlchemy** e **SQLite**, com autenticação via JWT, controle de acesso por usuário/administrador e versionamento de banco de dados com Alembic.

Cada usuário pode cadastrar, visualizar, editar e excluir seus próprios personagens de RPG (mago, guerreiro, lutador, etc.), enquanto administradores têm acesso irrestrito a todos os registros.

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
- Controle de permissão: cada usuário só acessa seus próprios personagens; administradores acessam todos

## Rotas principais

### Autenticação (`/auth`)
| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/criar_conta` | Cria um novo usuário |
| POST | `/auth/login` | Login via JSON (email e senha), retorna token JWT |
| POST | `/auth/login-form` | Login via formulário (usado pelo Swagger) |

### Personagens (`/personagens`) — requer autenticação
| Método | Rota | Descrição |
|---|---|---|
| POST | `/personagens/personagem` | Cria um novo personagem |
| GET | `/personagens/ver_personagem/{id}` | Visualiza um personagem (dono ou admin) |
| GET | `/personagens/listar` | Lista todos os personagens (somente admin) |
| GET | `/personagens/listar/personagens-usuario` | Lista os personagens do usuário logado |
| PUT | `/personagens/editar_personagem/{id}` | Edita um personagem (dono ou admin) |
| POST | `/personagens/personagem/excluir/{id}` | Exclui um personagem (dono ou admin) |

## Como rodar o projeto localmente

1. Clone o repositório:
```
git clone <link-do-repositorio>
cd API_cadastro_jogador
```

2. Crie e ative um ambiente virtual:
```
python -m venv .venv
.venv\Scripts\activate      # Windows
```

3. Instale as dependências:
```
pip install fastapi uvicorn sqlalchemy "passlib[bcrypt]" "python-jose[cryptography]" python-dotenv python-multipart alembic
```

4. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Rode as migrations para criar o banco de dados:
```
alembic upgrade head
```

6. Inicie o servidor:
```
uvicorn main:app --reload
```

7. Acesse a documentação interativa (Swagger) em:
```
http://127.0.0.1:8000/docs
```

## Testes

Os testes foram realizados manualmente via Swagger, validando os fluxos de cadastro, login e CRUD de personagens.

## Próximos passos

- Implementar testes automatizados com pytest e httpx
- Containerizar a aplicação com Docker
- Restringir a criação de administradores apenas a usuários administradores

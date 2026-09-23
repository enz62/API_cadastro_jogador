from fastapi import APIRouter, Depends, HTTPException 
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth",tags=["auth"])

def criar_token(id_usuario, duracao_token = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub" : str(id_usuario) , "exp" : data_expiracao}
    jwt_codificado = jwt.encode(dic_info , SECRET_KEY, ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session:Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha,usuario.senha):
        return False
    return usuario


@auth_router.get("/")
async def autenticar():
    """
    essa é a rota padrão de autenticação do sistema
    """
    return {"mensagem" : "você acessou a rota padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema,session:Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail = "E-mail de usuário ja cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome,usuario_schema.email,senha_criptografada, usuario_schema.ativo, admin = False)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem" : f"usuário cadastrado com sucesso {usuario_schema.email}"}

@auth_router.put("/promover_admin/{id_usuario}")
async def promover_admin(id_usuario: int , session: Session = Depends(pegar_sessao), usuario_logado: Usuario = Depends(verificar_token)):
    if not usuario_logado.admin == True:
        raise HTTPException(status_code = 401, detail = "Apenas Administradores podem promover outros usuários")
    else:
        usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()

        if not usuario:
            raise HTTPException(status_code = 400, detail = "Usuario selecionado não existe")

        usuario.admin = True
        session.commit()
        return {"mensagem" : f"Usuario {usuario.id} promovido a administrador"}
    

@auth_router.post("/login")
async def login(login_schema: LoginSchema,  session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email,login_schema.senha,session)
    if not usuario:
        raise HTTPException(status_code=400, detail = "Usuario não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token" : access_token, 
            "token_type" : "Bearer"
            }

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(),  session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username,dados_formulario.password,session)
    if not usuario:
        raise HTTPException(status_code=400, detail = "Usuario não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token" : access_token,
            "token_type" : "Bearer"
            }

@auth_router.post("/usuario/deletar/{id_usuario}")
async def deletar_usuario(id_usuario: int , session: Session = Depends(pegar_sessao), usuario : Usuario = Depends(verificar_token)):
    usuario_excluido = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario_excluido:
        raise HTTPException(status_code = 400 , detail = "usuario não encontrado")
    else:
        if usuario.id != id_usuario and usuario.admin == False:
            raise HTTPException(status_code = 401, detail = "Você não tem permissão para realizar essa ação")
        else:
            total_admins = session.query(Usuario).filter(Usuario.admin == True).count()
            if usuario_excluido.admin == True and total_admins <= 1:
                raise HTTPException(status_code=400, detail="Não é possível remover o último administrador do sistema")
            else:
                session.delete(usuario_excluido)
                session.commit()
                return {
                    "mensagem" : f"usuario {id_usuario} deletado com sucesso"
                }

@auth_router.put("/usuario/rebaixar/{id_usuario}")
async def rebaixar_usuario(id_usuario : int , session : Session = Depends(pegar_sessao), usuario : Usuario = Depends(verificar_token)):
    usuario_rebaixado = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario_rebaixado:
        raise HTTPException(status_code = 400 , detail = "O usuario selecionado não existe")
    elif usuario.admin == False:
        raise HTTPException(status_code = 401 , detail = "você não tem permissão para realizar essa ação")
    else:
        total_admins = session.query(Usuario).filter(Usuario.admin == True).count()
        if usuario_rebaixado.admin == True and total_admins <= 1:
            raise HTTPException(status_code=400, detail="Não é possível remover o último administrador do sistema")
        else:
            usuario_rebaixado.admin = False
            session.commit()
            return {
                "mensagem" : f"o usuario {id_usuario} foi rebaixado para um usuário normal"
            } 
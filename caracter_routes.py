from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PersonagemSchema, ResponsePersonagemSchema
from models import Personagem, Usuario
from typing import List

order_router = APIRouter(prefix="/personagens",tags = ["personagem"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def personagens():
    """
    Essa é a rota padrão de criação de personagem. Toda rota de criação de personagem precisa de autenticação
    """
    return {"mensagem": "Você acessou a rota de criação de personagem"}

@order_router.post("/personagem")
async def criar_personagem(personagem_schema: PersonagemSchema, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    novo_personagem = Personagem(usuario.id,personagem_schema.nome,personagem_schema.classe,personagem_schema.arma)
    session.add(novo_personagem)
    session.commit()
    return {"mensagem" : f"Personagem criado com sucesso. ID do personagem: {novo_personagem.id}"}

@order_router.post("/personagem/excluir/{id_personagem}")
async def excluir_personagem(id_personagem: int, session : Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    personagem = session.query(Personagem).filter(Personagem.id==id_personagem).first()
    if not personagem:
        raise HTTPException(status_code = 400, detail = "Personagem não encontrado")
    if not usuario.admin and usuario.id != personagem.usuario_id:
        raise HTTPException(status_code = 401, detail = "Você não tem autoriação para fazer essa modificação")
    
    session.delete(personagem)
    session.commit()
    return {
        "mensagem" : f"Personagem numero {personagem.id} excluido com sucesso",
        "personagem" : personagem
    }

@order_router.get("/listar", response_model = List[ResponsePersonagemSchema])
async def listar_todos(session: Session = Depends(pegar_sessao), usuario:Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code = 401, detail = "Você não tem autorização para realizar essa operação")
    else:
        personagens = session.query(Personagem).all()
        return personagens
        

@order_router.get("/ver_personagem/{id_personagem}", response_model = ResponsePersonagemSchema)
async def visualizar_personagem(id_personagem: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    personagem = session.query(Personagem).filter(Personagem.id==id_personagem).first()
    if not personagem:
        raise HTTPException(status_code = 400, detail = "Personagem não encontrado")
    if not usuario.admin and usuario.id != personagem.usuario_id:
        raise HTTPException(status_code = 401, detail = "Você não tem autoriação para ver este personagem")
    return personagem
    

@order_router.get("/listar/personagens-usuario", response_model=List[ResponsePersonagemSchema])
async def listar_personagens(session: Session = Depends(pegar_sessao), usuario:Usuario = Depends(verificar_token)):
        personagens = session.query(Personagem).filter(Personagem.usuario_id==usuario.id).all()
        return personagens

@order_router.put("/editar_personagem/{id_personagem}")
async def editar_personagem(personagemschema: PersonagemSchema , id_personagem:int , session: Session = Depends(pegar_sessao), usuario:Usuario = Depends(verificar_token)):
    personagem = session.query(Personagem).filter(Personagem.id==id_personagem).first()
    if not personagem:
        raise HTTPException(status_code = 400, detail = "personagem não encontrado")
    if not usuario.admin and usuario.id != personagem.usuario_id:
        raise HTTPException(status_code = 400, detail = "Você não tem permissão para alterar este usuário")

    personagem.nome = personagemschema.nome
    personagem.classe = personagemschema.classe
    personagem.arma = personagemschema.arma
    session.commit()
    return {
        "mensagem": "Alteração realizada com sucesso"
        }
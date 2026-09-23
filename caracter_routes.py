from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PersonagemSchema, ResponsePersonagemSchema, AtributosSchema
from models import Personagem, Usuario, Atributos
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
    novo_personagem.atributos = Atributos(vida=0, escudo=0, vigor=0, sorte=0, inteligencia=0, forca=0)
    novo_personagem.calcular_atributos()

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

@order_router.put("/editar_personaagem/editar_atributos/{id_personagem}")
async def editar_atributos(atributosschema: AtributosSchema , id_personagem : int , session : Session = Depends(pegar_sessao), usuario:Usuario = Depends(verificar_token)):
    personagem = session.query(Personagem).filter(Personagem.id == id_personagem ).first()
    if not personagem:
        raise HTTPException(status_code = 400, detail = "personagem não encontrado")
    elif usuario.admin == False and  personagem.usuario_id != usuario.id:
        raise HTTPException(status_code = 401 , detail = "Você não tem permissão para realizar essa alteração")
    else:
        atributos_personagem = session.query(Atributos).filter(Atributos.id_personagem == id_personagem).first()
        if atributosschema.vida is not None:
            atributos_personagem.vida = atributosschema.vida
        if atributosschema.escudo is not None:
            atributos_personagem.escudo = atributosschema.escudo
        if atributosschema.vigor is not None:
            atributos_personagem.vigor = atributosschema.vigor
        if atributosschema.forca is not None:
            atributos_personagem.forca = atributosschema.forca
        if atributosschema.inteligencia is not None:
            atributos_personagem.inteligencia = atributosschema.inteligencia
        if atributosschema.sorte is not None:
            atributos_personagem.sorte = atributosschema.sorte
        personagem.calcular_atributos()
        session.commit()
        return {
            "mensagem" : f"os atributos do personagem {id_personagem} foram atualizados",
            "vida" : atributos_personagem.vida,
            "escudo" : atributos_personagem.escudo,
            "vigor" : atributos_personagem.vigor,
            "forca" : atributos_personagem.forca,
            "inteligencia" : atributos_personagem.inteligencia,
            "sorte" : atributos_personagem.sorte 
        }
    

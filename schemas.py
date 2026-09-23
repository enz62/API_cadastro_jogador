from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class PersonagemSchema(BaseModel):
    nome: str
    classe: str
    arma: str 

    class Config:
        from_attributes = True


class AtributosSchema(BaseModel):
    vida: Optional[int] = None
    escudo: Optional[int] = None
    vigor: Optional[int] = None
    sorte: Optional[int] = None
    inteligencia: Optional[int] = None
    forca: Optional[int] = None

    class Config:
        from_attributes = True

class ResponseAtributosSchema(BaseModel):
    vida: int
    escudo: int
    vigor: int
    sorte: int
    inteligencia: int
    forca: int
    
    class Config:
        from_attributes = True

class ResponsePersonagemSchema(BaseModel):
    id: int
    nome: str
    classe: str
    arma: str
    atributos: ResponseAtributosSchema
    atributos_totais: Optional[int]

    class Config:
        from_attributes = True




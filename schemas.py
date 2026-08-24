from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

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

class ResponsePersonagemSchema(BaseModel):
    id: int
    nome: str
    classe: str
    arma: str

    class Config:
        from_attributes = True
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base
db = create_engine("sqlite:///banco.db")

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key= True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email" , String, nullable= False)
    senha = Column("senha", String, nullable= False)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default = False)

    def __init__(self,nome,email,senha,ativo=True,admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Personagem(Base):
    __tablename__ = "personagens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(ForeignKey("usuarios.id"), nullable=False)
    nome = Column(String, nullable=False)
    classe = Column(String, nullable=False)
    arma = Column(String, nullable=True)

    def __init__(self, usuario_id, nome, classe, arma=None):
        self.usuario_id = usuario_id
        self.nome = nome
        self.classe = classe
        self.arma = arma

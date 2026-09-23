from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
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
    personagens = relationship("Personagem", cascade="all, delete-orphan")

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
    arma = Column(String, nullable=False)
    atributos_totais = Column("Atributos_Totais",Integer)
    atributos = relationship("Atributos", uselist = False ,cascade = "all, delete")

    def __init__(self, usuario_id, nome, classe, arma=None):
        self.usuario_id = usuario_id
        self.nome = nome
        self.classe = classe
        self.arma = arma

    def calcular_atributos(self):
        self.atributos_totais = (
        self.atributos.vida + self.atributos.escudo + self.atributos.vigor +
        self.atributos.sorte + self.atributos.inteligencia + self.atributos.forca
    )

class Atributos(Base):

    __tablename__ = "atributos"

    
    id_personagem = Column("id_personagem", ForeignKey("personagens.id"), primary_key = True)
    vida = Column("Vida", Integer)
    escudo = Column("Escudo", Integer)
    vigor = Column("Vigor", Integer)
    sorte = Column("Sorte", Integer)
    inteligencia = Column("Inteligencia", Integer)
    forca = Column("Forca", Integer)

    def __init__(self,vida,escudo,vigor,sorte,inteligencia,forca):
        self.vida = vida
        self.escudo = escudo
        self.vigor = vigor
        self.sorte = sorte
        self.inteligencia = inteligencia
        self.forca = forca


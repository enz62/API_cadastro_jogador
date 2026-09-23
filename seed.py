from models import db, Usuario
from sqlalchemy.orm import sessionmaker
from main import bcrypt_context

email_padrao = "admin123@gmail.com"
senha_padrao = "123abc"

Session = sessionmaker(bind=db)
session = Session()

usuario = session.query(Usuario).filter(Usuario.admin == True).first()
if usuario:
    print("ja existe uma conta admin")
else:
    senha_criptograda = bcrypt_context.hash(senha_padrao)
    novo_admin = Usuario("admin",email_padrao,senha_criptograda,ativo = True , admin = True)
    session.add(novo_admin)
    session.commit()
    session.close()
    print("O usuário admin foi criado com sucesso")



from flask import Flask # cria o site
from flask_sqlalchemy import SQLAlchemy # gerencia o banco de dados
from flask_login import LoginManager  #gerencia a autenticação
from flask_bcrypt import Bcrypt  #criptografa as senhas

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cadastro.db" # Define o banco de dados usando SQLite
app.config["SECRET_KEY"] = "037545bf136aaafa4f2bdda083c88b7b"  # chave secreta usada pelo Flask para criptografar sessões e formulários



databse = SQLAlchemy(app)               # interface para manipular o banco de dados.
bcrypt = Bcrypt(app)                    # hash de senha seguro.
login_manager = LoginManager(app)       # gerencia sessões de login.
login_manager.login_view = 'homepage'   # indica que, se um usuário não estiver logado, ele será redirecionado para a homepage

from ecommerce import routes  # impotação das rotas
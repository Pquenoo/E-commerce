#criando a estrutura do bando de dados

from ecommerce import databse,login_manager
from flask_login import  UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(databse.Model, UserMixin):
    __tablename__ = 'usuario'

    id = databse.Column(databse.Integer, primary_key=True)
    username = databse.Column(databse.String(50), nullable=True)
    email = databse.Column(databse.String(120), nullable=True, unique=True)
    password = databse.Column(databse.String(128), nullable=True)

    # Um usuário pode ter vários produtos
    produtos = databse.relationship('Produto', backref='usuario', lazy=True)

class Produto(databse.Model):
    __tablename__ = 'produto'

    id = databse.Column(databse.Integer, primary_key=True)
    nome = databse.Column(databse.String(100), nullable=True)
    valor = databse.Column(databse.Float, nullable=True)

    # Chave estrangeira ligando ao usuário
    usuario_id = databse.Column(databse.Integer, databse.ForeignKey('usuario.id'), nullable=False)

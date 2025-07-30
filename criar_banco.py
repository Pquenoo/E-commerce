from ecommerce import databse,app
from ecommerce.models import Usuario, Produto

with app.app_context():
    databse.drop_all()
    databse.create_all()


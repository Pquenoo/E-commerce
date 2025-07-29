from ecommerce import databse,app
from ecommerce.models import Usuario, Produto

with app.app_context():
    databse.create_all()

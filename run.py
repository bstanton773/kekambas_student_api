from app import app, db
from app.models import Kekambas, Posts
from app.blueprints.api.models import Product, User


@app.shell_context_processor
def create_context():
    return {
        'db': db,
        'Kekambas': Kekambas,
        'Posts': Posts,
        'User': User,
        'Product': Product
    }
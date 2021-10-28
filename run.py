from app import app, db
from app.models import Kekambas, Posts


@app.shell_context_processor
def create_context():
    return {
        'db': db,
        'Kekambas': Kekambas,
        'Posts': Posts
    }
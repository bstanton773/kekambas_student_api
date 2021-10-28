from app import db
from datetime import datetime as dt

class Kekambas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    posts = db.relationship('Posts', backref='user', lazy='dynamic')


    def __init__(self, first, last):
        self.first_name = first
        self.last_name = last

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(), default=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('kekambas.id'))

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date_created': self.date_created,
            'user': Kekambas.query.get(self.user_id).to_dict()
        }
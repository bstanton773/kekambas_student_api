from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import cross_origin
from config import Config
from datetime import datetime as dt

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

    def __init__(self, first, last):
        self.first_name = first
        self.last_name = last

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date_created': self.date_created,
            'user': Kekambas.query.get(self.user_id).to_dict()
        }


@app.route('/')
def index():
    return 'Hello World'

@app.route('/kekambas')
@cross_origin()
def kekambas():
    students = [k.to_dict() for k in Kekambas.query.all()]
    return jsonify(students)

@app.route('/posts')
@cross_origin()
def posts():
    posts = [p.to_dict() for p in Posts.query.all()]
    return jsonify(posts)

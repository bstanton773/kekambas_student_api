from app import app
from app.models import Kekambas, Posts
from flask import jsonify
from flask_cors import cross_origin

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
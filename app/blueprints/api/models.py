from sqlalchemy.orm import backref
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import base64
import os


cart = db.Table('cart',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(250))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    products = db.relationship('Product', secondary=cart, lazy=True, backref='users')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self, with_cart=False):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
        }
        if with_cart:
            data['cart'] = [p.to_dict() for p in self.products]
        return data

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'username', 'email', 'password']:
            if field in data:
                if field == 'password':
                    setattr(self, field, generate_password_hash(data[field]))
                else:
                    setattr(self, field, data[field])
        self.save()

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        db.session.commit()

    def add_to_cart(self, product):
        self.products.append(product)
        db.session.commit()

    def remove_from_cart(self, product):
        self.products.remove(product)
        db.session.commit()


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float())
    image = db.Column(db.String())
    description = db.Column(db.String())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, name, price, image, description):
        self.name = name
        self.price = price
        self.image = image
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'description': self.description,
            'created_on': self.created_on
        }
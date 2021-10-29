from . import bp as api
from .models import Product, User
from .auth import basic_auth, token_auth
from flask import jsonify, request


@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    current_user = basic_auth.current_user()
    token = current_user.get_token()
    return jsonify({'token': token})


####################
# ROUTES FOR USERS #
####################

@api.route('/users')
def users():
    return jsonify([u.to_dict() for u in User.query.all()])


@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    needed = {'first_name', 'last_name', 'username', 'email', 'password'}
    missing_keys = needed - set(data.keys())
    if missing_keys:
        return jsonify({'error': f'You are missing the following fields: {missing_keys}'}), 400
    existing_user = User.query.filter((User.username == data['username'])|(User.email == data['email'])).first()
    if existing_user:
        return jsonify({'error': 'A user with that username or email already exists'}), 400 
    new_user = User()
    new_user.from_dict(data)
    return jsonify(new_user.to_dict()), 201


@api.route('/users/me')
@token_auth.login_required
def get_me():
    user = token_auth.current_user()
    return jsonify(user.to_dict())


@api.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to update this user'}), 403
    data = request.json
    current_user.from_dict(data)
    return jsonify(current_user.to_dict())


@api.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to delete this user'}), 403
    current_user.delete()
    return jsonify({}), 204


#######################
# ROUTES FOR PRODUCTS #
#######################
@api.route('/products')
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@api.route('/products/<id>')
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

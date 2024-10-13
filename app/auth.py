import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from .models import User, RoleEnum
from . import db
from functools import wraps

auth_bp = Blueprint('auth', __name__)


def generate_token(user):
    token = jwt.encode({
        'user_id': user.id,
        'role': user.role.value,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return token

@auth_bp.route('/register', methods=['POST'], endpoint='register')
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists"}), 400
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        role=RoleEnum.ADMIN if data.get('is_admin') else RoleEnum.USER
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'], endpoint='login')
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        token = generate_token(user)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.get(data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(user, *args, **kwargs)
    return decorated

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected_route(user):
    return jsonify({"message": f"Welcome {user.username}, you have access!"}), 200


def admin_required(f):
    @wraps(f)
    def decorated(user, *args, **kwargs):
        if user.role != RoleEnum.ADMIN:
            return jsonify({"message": "Admin access required"}), 403
        return f(user, *args, **kwargs)
    return decorated

@auth_bp.route('/admin', methods=['GET'])
@token_required
@admin_required
def admin_route(user):
    return jsonify({"message": f"Welcome Admin {user.username}, you have access!"}), 200

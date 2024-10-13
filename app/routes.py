from flask import Blueprint, request, jsonify
from .models import User, Post, Tag
from .schemas import UserSchema, PostSchema, TagSchema
from .auth import token_required, admin_required
from . import db

api_bp = Blueprint('api', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

@api_bp.route('/users', methods=['POST'])
@token_required
@admin_required
def create_user():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']  
    )
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user), 201

@api_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users), 200

@api_bp.route('/users/<int:id>', methods=['GET'])
@token_required
@admin_required
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user), 200

@api_bp.route('/users/<int:id>', methods=['PUT'])
@token_required
@admin_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    
    db.session.commit()
    return user_schema.jsonify(user), 200

@api_bp.route('/users/<int:id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

@api_bp.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json()
    errors = post_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_post = Post(
        title=data['title'],
        content=data['content'],
        author_id=current_user.id
    )

    if 'tags' in data:
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            new_post.tags.append(tag)

    db.session.add(new_post)
    db.session.commit()
    
    return post_schema.jsonify(new_post), 201

@api_bp.route('/posts', methods=['GET'])
@token_required
def get_posts():
    posts = Post.query.all()
    return posts_schema.jsonify(posts), 200

@api_bp.route('/posts/<int:id>', methods=['GET'])
@token_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return post_schema.jsonify(post), 200

@api_bp.route('/posts/<int:id>', methods=['PUT'])
@token_required
@admin_required
def update_post(current_user, id):
    post = Post.query.get_or_404(id)
    if post.author_id != current_user.id and current_user.role != RoleEnum.ADMIN:
        return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    errors = post_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)

    if 'tags' in data:
        post.tags.clear()
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            post.tags.append(tag)

    db.session.commit()
    return post_schema.jsonify(post), 200

@api_bp.route('/posts/<int:id>', methods=['DELETE'])
@token_required
@admin_required
def delete_post(current_user, id):
    post = Post.query.get_or_404(id)
    if post.author_id != current_user.id and current_user.role != RoleEnum.ADMIN:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200

@api_bp.route('/tags', methods=['POST'])
@token_required
def create_tag(current_user):
    data = request.get_json()
    errors = tag_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_tag = Tag(name=data['name'])
    db.session.add(new_tag)
    db.session.commit()
    
    return tag_schema.jsonify(new_tag), 201

@api_bp.route('/tags', methods=['GET'])
@token_required
def get_tags():
    tags = Tag.query.all()
    return tags_schema.jsonify(tags), 200

@api_bp.route('/tags/<int:id>', methods=['PUT'])
@token_required
@admin_required
def update_tag(id):
    tag = Tag.query.get_or_404(id)
    data = request.get_json()
    errors = tag_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    tag.name = data['name']
    db.session.commit()
    return tag_schema.jsonify(tag), 200

@api_bp.route('/tags/<int:id>', methods=['DELETE'])
@token_required
@admin_required
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "Tag deleted"}), 200

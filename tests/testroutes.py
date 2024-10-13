import pytest
from app import create_app, db
from app.models import User, Post, Tag, RoleEnum
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture
def admin_token(client):
    admin = User(username='admin', email='admin@test.com', role=RoleEnum.ADMIN)
    admin.set_password('password123')
    db.session.add(admin)
    db.session.commit()
    return create_access_token(identity=admin)

@pytest.fixture
def user_token(client):
    user = User(username='user', email='user@example.com', role=RoleEnum.USER)
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return create_access_token(identity=user)

def test_register_user(client):
    response = client.post('/auth/register', json={
        'username': 'ariel',
        'email': 'ariel@test.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert 'User registered successfully' in response.json['message']

def test_login_user(client):
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.json

def test_create_user(client, admin_token):
    response = client.post('/users', json={
        'username': 'chrit',
        'email': 'christ@test.com',
        'password': 'password123'
    }, headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 201
    assert response.json['username'] == 'christ'

def test_get_users(client, admin_token):
    response = client.get('/users', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_post(client, user_token):
    response = client.post('/posts', json={
        'title': 'post de test',
        'content': 'Ceci est un post de test',
        'tags': ['test', 'example']
    }, headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 201
    assert response.json['title'] == 'post de test'

def test_get_posts(client, user_token):
    response = client.get('/posts', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_tag(client, admin_token):
    response = client.post('/tags', json={
        'name': 'nouveau tag de test'
    }, headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 201
    assert response.json['name'] == 'nouveau tag de test'

def test_get_tags(client, user_token):
    response = client.get('/tags', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert isinstance(response.json, list)



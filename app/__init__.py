from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config import Config

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    migrate = Migrate(app, db)

    from .routes import api_bp
    from .auth import auth_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    @app.route('/')
    def home():
        home_template = '''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Accueil - API Flask</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #f8f9fa;
                    color: #333;
                    display: flex;
                    flex-direction: column;
                    min-height: 100vh;
                }
                .content {
                    flex: 1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .container {
                    background-color: white;
                    border-radius: 15px;
                    padding: 2rem;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                    max-width: 800px;
                }
                h1 {
                    color: #007bff;
                }
                .btn-primary {
                    background-color: #007bff;
                    border-color: #007bff;
                }
                .btn-primary:hover {
                    background-color: #0056b3;
                    border-color: #0056b3;
                }
                footer {
                    background-color: #343a40;
                    color: white;
                    text-align: center;
                    padding: 1rem 0;
                    margin-top: 2rem;
                }
            </style>
        </head>
        <body>
            <div class="content">
                <div class="container text-center">
                    <h1 class="mb-4">Bienvenue sur notre API Flask</h1>
                    
                    <h2 class="h4 mb-3">Fonctionnalités principales :</h2>
                    <ul class="list-unstyled mb-4">
                        <li>✅ Gestion complète des utilisateurs (création, modification, suppression)</li>
                        <li>🔐 Authentification sécurisée avec JWT (JSON Web Tokens)</li>
                        <li>📝 CRUD complet pour les posts (Création, Lecture, Mise à jour, Suppression)</li>
                        <li>🏷️ Système de tags pour catégoriser les posts</li>
                        <li>👥 Gestion des autorisations basée sur les rôles (utilisateur, administrateur)</li>
                    </ul>
                    
                    <a href="/swagger" class="btn btn-primary btn-lg">Accéder à la documentation Swagger</a>
                </div>
            </div>
            
            <footer>
                <div >
                    <p class="mb-0">Copyright © 2024</p>
                    <p class="mb-0">Développé par Ariel Christ NGATO</p>
                </div>
            </footer>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        '''
        return render_template_string(home_template)
    
    return app

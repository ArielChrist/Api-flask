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
        </head>
        <body>
            <div class="container mt-5">
                <h1 class="mb-4">Bienvenue sur notre API Flask</h1>
                <p class="lead">Cette API offre des fonctionnalités d'authentification et de gestion des utilisateurs.</p>
                <a href="/swagger" class="btn btn-primary">Accéder à la documentation Swagger</a>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        '''
        return render_template_string(home_template)
    
    return app

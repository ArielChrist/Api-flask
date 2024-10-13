from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger/'
API_URL = '/static/swagger.json' 

def setup_swagger(app):
    swagger_ui_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui_bp, url_prefix=SWAGGER_URL)

from app import create_app
from app.utils import setup_swagger

app = create_app()
setup_swagger(app)

if __name__ == '__main__':
    app.run()

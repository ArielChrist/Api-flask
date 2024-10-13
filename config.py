import os 
from dotenv import load_dotenv

load_dotenv()

class Config: 
    FLASK_DEBUG=os.getenv('FLASK_DEBUG')
    FLASK_ENV=os.getenv('FLASK_ENV')
    FLASK_APP=os.getenv('FLASK_APP')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')

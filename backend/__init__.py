from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager
from flask_migrate    import migrate
from sqlalchemy       import create_engine
from backend.config   import *

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config,py')

    engine = create_engine(app.config['DB_URL'], encoding = 'utf-8')
    app.database = engine

    migrate.init_app(app. db)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'

    db.init_app(app)

    from website.views import views
    from website.auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
  
    from website.models import User

    if database_exists('sqlite:///database.db'):
        print('Database already exists')
    else:
        with app.app_context():
            db.create_all()
            print('Database was created')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
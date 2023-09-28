'''__init__ function that stores create_app function and solidifies the database.'''
from os import path
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    '''Create App function that is called through main.py'''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '128903468901234'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')

    return app

def create_database(app):
    if not path.exists('instance' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')

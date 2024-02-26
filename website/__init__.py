from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

from website.utils.template_funcs import get_dict_val

db = SQLAlchemy()
login_manager = LoginManager()
DB_NAME = "database.db"
app = Flask(__name__, 
            static_url_path='', 
            static_folder='static')
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.jinja_env.globals.update(get_dict_val=get_dict_val)



def create_app():
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

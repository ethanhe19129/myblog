from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/myblog"
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "you guess"
    db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
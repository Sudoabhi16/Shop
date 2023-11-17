from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from elecshop.config import Config
from flask_mail import Mail


# app.config['SECRET_KEY'] = '02207f7dd889ad65fe1ab14e5a74a44d'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "users.login"
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # with app.app_context():
    #     db.create_all()

    from elecshop.users.routes import users
    from elecshop.shop.routes import shop
    from elecshop.admin.routes import admin

    app.register_blueprint(users)
    app.register_blueprint(shop)
    app.register_blueprint(admin)

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
import os 

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # apúntalo al blueprint de login


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu_clave_segura_aqui'

    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance")
    os.makedirs(instance_path, exist_ok=True)
    db_path = os.path.join(instance_path, "tecnico.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    Bootstrap5(app)

    from app.models import User

    # Registrar user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    # importar blueprints
    from .routes.auth import auth
    from .routes.dashboard import dashboard
    from .routes.core import core

    # registrar blueprints
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(core)

    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__,
            template_folder='web',
            static_folder='web/static')
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Регистрация user_loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Импортируем здесь, чтобы избежать циклических импортов
        return User.query.get(int(user_id))

    # Регистрация маршрутов
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.voting import voting_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(voting_bp)
    app.register_blueprint(main_bp) # Регистрация Blueprint main

    return app

from flask import Flask
from flask_qa.models.question import Question
from flask_qa.models.user import User
from .config.config import Config
from .utils import db, login_manager, migrate
from .qa.views import q_a
from .auth.views import auth

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)
   
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(q_a)
    app.register_blueprint(auth)

    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Question': Question
        }

    return app
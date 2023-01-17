from flask import Flask
from flask_qa.models.question import Question
from flask_qa.models.user import User
from .config.config import Config
from .utils import db, login_manager, migrate
from .qa.views import q_a
from .auth.views import auth
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler

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

    with app.app_context():
        db.create_all()

    # configure_logging(app)

    
    # @app.shell_context_processor
    # def make_shell_context():
    #     return {
    #         'db': db,
    #         'User': User,
    #         'Question': Question
    #     }

    return app


# def configure_logging(app):
#     # Logging Configuration
#     if app.config['LOG_WITH_GUNICORN']:
#         gunicorn_error_logger = logging.getLogger('gunicorn.error')
#         app.logger.handlers.extend(gunicorn_error_logger.handlers)
#         app.logger.setLevel(logging.DEBUG)
#     else:
#         file_handler = RotatingFileHandler('instance/flask-test-app.log',
#                                         maxBytes=16384,
#                                         backupCount=20)
#         file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]')
#         file_handler.setFormatter(file_formatter)
#         file_handler.setLevel(logging.INFO)
#         app.logger.addHandler(file_handler)

#     # Remove the default logger configured by Flask
#     app.logger.removeHandler(default_handler)

#     app.logger.info('Starting the Flask Test App...')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv() # Upload environment variables

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    from app.models.company import Company
    from app.models.user import User
    # Create an instance folder for the local test database
    # import os if you want to create the instance folder
    # instance_path = os.path.join(os.getcwd(), 'instance')
    # os.makedirs(instance_path, exist_ok=True)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("app.config.Config")

    # Set max session lifetime when a user remembers their password
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controllers.company_controller import company_bp
    from app.controllers.user_controller import user_bp

    app.register_blueprint(company_bp)
    app.register_blueprint(user_bp)

    return app
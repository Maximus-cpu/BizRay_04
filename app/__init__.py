import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    #Create instance folder for database and environment files
    instance_path = os.path.join(os.getcwd(), 'instance')
    os.makedirs(instance_path, exist_ok=True)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    from app.controllers.company_controller import main_bp
    app.register_blueprint(main_bp)

    return app
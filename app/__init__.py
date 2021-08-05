"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from config import DevelopementConfig
import os, config

db = SQLAlchemy()
migrate = Migrate()

# application factory
def create_app():
    # create application instance
    app = Flask(__name__)
    app.config.from_object(DevelopementConfig)

    # Initialize plugins
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        # import our utils.py file
        #from utils.utility_fxns import validate_image, my_decode_text, encode_text

        # Create database tables for our data models
        #db.create_all()

        return app


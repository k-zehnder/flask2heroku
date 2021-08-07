"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os, config
from os import environ
from peewee import *
from playhouse.db_url import connect # needed for peewee in heroku

#db = SQLAlchemy()
url = os.environ.get("DATABASE_URL") 
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
db = connect(url)

# application factory
def create_app():
    # create application instance
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize plugins
    #db.init_app(app)

    with app.app_context():

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        # import our utils.py file
        #from utils.utility_fxns import validate_image, my_decode_text, encode_text

        # Create database tables for our data models
        #db.create_all()

        return app


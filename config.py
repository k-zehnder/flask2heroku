import os
from dotenv import load_dotenv
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# USER = "zelda" or os.environ.get("USER")
# PASS = "password" or os.environ.get("PASS")
# HOST = "localhost" or os.environ.get("HOST")
# PORT = 5432 or os.environ.get("PORT")
# DB = "patient" or os.environ.get("DB")
# db_string = f"postgres://{USER}:{PASS}@{HOST}:{PORT}/{DB}"

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
    PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
    JSON_PATH = os.environ.get("JSON_PATH")
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = os.environ.get("FLASK_ENV")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # or db_string

# class DevelopementConfig(Config):
#     DEBUG = os.environ.get("FLASK_ENV")
#     SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') # or db_string

# class TestingConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
#                               'mysql+pymysql://root:pass@localhost/flask_app_db'    

# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or  \
#         'mysql+pymysql://root:pass@localhost/flask_app_db'


"""
DRIVER = "postgresql"  # Dont change this ,Not recomended
host = os.environ.get("PSQL_HOST","localhost")
port = os.environ.get("PSQL_PORT",5432)
username = os.environ.get("PSQL_USERNAME","postgres")
password = os.environ.get("PSQL_PASSWORD","password123")

db_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(db_uri, echo=True)

    
https://github.com/k-zehnder/BuzzNet/blob/3811cbbaaea5d962ce650b9243449b20108d0906/timezone_conversion/initdb.py

from peewee import *
from models import db, Patient
from utils import *

# initialize db
db = SqliteDatabase('respondNoTwilio.db')
db.connect()

# query all users and print them
print("\n[INFO] Querying and printing all users...")
query_all()

#now = datetime.datetime.utcnow()
query = (Patient
         .select(Patient.username, Patient.phone, Patient.timezone, Patient.timestamp, Patient.utc_start, Patient.utc_end)
         .where(
            Patient.timezone == "US/Pacific", Patient.utc_start < datetime.datetime.utcnow()) 
            )

print("\n[INFO] Querying only US/Pacific users...")
for (i, row) in enumerate(query):
   print(i, f"name: {row.username} phone: {row.phone} timezone: {row.timezone} timestamp: {row.timestamp}    utc_start: {row.utc_start} utc_end: {row.utc_end}\n")

db.close()

"""
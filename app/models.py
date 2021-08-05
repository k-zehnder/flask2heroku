from peewee import *
import pandas as pd
import numpy as np
import datetime
from playhouse.db_url import connect
import os

"""Note: from playhouse.db_url import connect
important import for using peewee in heroku"""

db = connect(os.environ.get("DATABASE_URL")) # db = connect(os.environ.get('DATABASE_URL'))

# Base model for work with Database through ORM
class BaseModel(Model):
    class Meta:
        database = db  # connection with database

class Patient(BaseModel):
    id = AutoField(column_name='ID')
    phone = TextField(column_name='Phone', null=True)
    username = TextField(column_name='Username', null=True)
    #gender = TextField(column_name='Gender', null=True)
    timezone = TextField(column_name='Timezone', null=True)
    timestamp = DateTimeField(column_name='Timestamp', default=datetime.datetime.utcnow, null=False) # NEW FIELD
    utc_start = TimeField(column_name='UTC_Start', null=True) # NEW FIELD
    utc_end = TimeField(column_name='UTC_End', null=True) # NEW FIELD
    #duration = TimeField(column_name='Duration', null=True) # NEW FIELD
    #callstart = TimeField(column_name='CallStart', null=True)
    #callend = TimeField(column_name='CallEnd', null=True)
    type = TextField(column_name='Type', null=True)
    #created = DateTimeField(column_name='Created', null=True)
    #updated = DateTimeField(column_name='Updated', null=True)
    class Meta:
        table_name = 'Patient'




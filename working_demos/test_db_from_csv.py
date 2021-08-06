from peewee import *
import datetime
import pandas as pd
# GoogleSheetHelper
import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from os import environ

class GoogleSheetHelper:
    """Helper class to pull data from googlesheets"""
    def __init__(self, cred_json, spreadsheetName):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.cred_json = cred_json
        self.spreadsheetName = spreadsheetName
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.cred_json, self.scope)
        self.client = gspread.authorize(self.creds)
        self.spreadsheet = self.client.open(self.spreadsheetName)

    def getDataframe(self,worksheet):
        """Returns all rows data from sheet as dataframe"""
        sheet = self.spreadsheet.worksheet(worksheet)
        rows = sheet.get_all_records()
        return pd.DataFrame(rows)

    def getAllWorksheet(self):
        # spreadsheet = self.client.open(self.spreadsheetName)
        return [s.title for s in self.spreadsheet.worksheets()] 

    def getAllSpreadsheets(self):
        """Returns sheets this gspread (self.client) authorized to view/edit"""
        available_sheets = self.client.openall()
        print(available_sheets)
        return [sheet.title for sheet in available_sheets]


from app.models import Patient

db = PostgresqlDatabase('patient', user='zelda', password="password", host='127.0.0.1', port=5432) 
db.connect()
# db.drop_tables([Patient])
db.create_tables([Patient])

df = pd.read_csv("/home/batman/Desktop/flask2heroku/users_test.csv")
df_dict = df.to_dict('records')

for d in df_dict:
    p = Patient(
            username=d["Username"], 
            utc_start=d["UTC start"],
            utc_end=d["UTC end"],
            phone=d["Number"],
            timezone=d["time zone"]
            )
    p.save() # each row now stored in database

db.close()
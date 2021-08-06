import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import sqlalchemy as sa
# from sqlalchemy.engine import make_url
# from sqlalchemy.types import Integer, Text, String, DateTime
import datetime


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


cred_json = "/home/batman/Desktop/flask2heroku/data/key.json"
gsh = GoogleSheetHelper(cred_json, "users_test")
print(gsh.getAllSpreadsheets())
print(gsh.getDataframe("users_test"))

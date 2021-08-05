import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import datetime
import pandas as pd
from pytz import timezone
import phonenumbers
from phonenumbers import geocoder
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

recipient_list = ['goandtodo@googlegroups.com']

sender_mail = 'heartvoices.org@gmail.com'
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


def send_mail(mail_type, phone, feedback=''):
    """
    Function is used for sending the mail when the user is created and the user gives feedback
    the type of the mail is decided by mail_type of the argument.
    """
    phone = str(phone[0:5] + '*****' + phone[10:])
    if mail_type == 'FEEDBACK':
        with open('templates/feedback.html', 'r') as template:
            html = ''.join(template.readlines())
            message = Mail(
                from_email=sender_mail,
                to_emails=recipient_list,
                subject=mail_type,
                html_content=html.format(phone=phone, feedback=feedback))

    elif mail_type == 'NEW USER':
        with open('templates/welcome.html', 'r') as template:
            html = ''.join(template.readlines())
            message = Mail(
                from_email=sender_mail,
                to_emails=recipient_list,
                subject=mail_type,
                html_content=html.format(phone=phone))
    else:
        print("Please check the mail_type before sending mail")
        return
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        if response.status_code == 202:
            print('send successfully')
    except Exception as e:
        print(e)


# helper class
class TimeZoneHelper:
    def __init__(self, phoneNumber):
        self.phoneNumber = phoneNumber
        self.tzs_df = pd.read_csv("data/tzmapping.csv")
        self.tzs_df.index = self.tzs_df['State']
        self.user_zone = self.numberToTimeZone()
        self.fmt = '%Y-%m-%d %H:%M:%S %Z%z'

    def numberToTimeZone(self):
        """This function converts a phone number to a timezone"""
        fmtNum = phonenumbers.parse("+" + str(self.phoneNumber))
        state = geocoder.description_for_number(fmtNum, 'en')
        time_zone = self.tzs_df.loc[state]['Zone'].split(" ")[0]
        return "US/" + time_zone

    def utcToLocal(self):
        """This function gets current local time from utc time given a zone in 24-hour time format"""
        # get utc time
        utc_dt = datetime.datetime.utcnow()
        # convert to localtime using tz object and string formatter
        zone_objct = timezone(self.user_zone)
        loc_dt = utc_dt.astimezone(zone_objct)
        return loc_dt.strftime(self.fmt)


# helper function to get temporary User data
def getTemporaryUserData():
    """This function gets temporary data from google sheet with proper formatting of User data"""
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('data/master_key.json', scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1M-IQ-iYji-dbJSkrPehh3CMLiLGlzWZBzzGqVWzJPog/edit?usp=sharing")
    # get all worksheets
    sheet_instance = sheet.worksheets()
    # convert to dataframe
    dataframe = pd.DataFrame(sheet_instance[0].get_all_records())
    return dataframe


# helper function to find appropriate match from temporary User data
def matchFromDf(dataframe, tz_from, verbose=False):
    """This function gets a match for user to call"""
    df = dataframe
    df[["DT Start"]] = df[["UTC start"]].apply(pd.to_datetime)
    df[["DT End"]] = df[["UTC end"]].apply(pd.to_datetime)

    # get current UTC time and find match
    now_utc = datetime.datetime.utcnow()
    tz = tz_from.numberToTimeZone()  # tz = "US/Pacific"
    mask = (df['DT Start'] < now_utc) & (df['DT End'] >= now_utc) & (df['time zone'] == tz)
    result = df.loc[mask]
    match = result.head(1)
    match = int(match['Number'])

    # log to console if necessary (default=False)
    if verbose:
        print(f"dataframe shape {dataframe.shape}")  # all results shape
        print(f"result shape: {result.shape}")  # candidate matches shape

    return match


def call_duration_from_api(phone):
    """
    The function is used for fetching the call duration for a particular number from the call log API of
    twilio and sum up the duration for the day and return it.
    """
    if phone:
        client = Client(account_sid, auth_token)
        date = datetime.datetime.today()
        calls = client.calls.list(from_=str(phone),
                                  start_time_after=datetime.datetime(date.year, date.month, date.day, 0, 0, 0))
        duration = 0
        for record in calls:
            duration += int(record.duration)
        return duration
    raise ValueError("No valid phone number found")
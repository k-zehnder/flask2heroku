import os
from datetime import datetime
from peewee import *
from twilio.twiml.voice_response import VoiceResponse, Dial, Gather, Say, Client
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from dotenv import load_dotenv
from app import db
from app.models import Patient
from app.main import bp
from playhouse.db_url import connect # needed for peewee in heroku
from app.utils.utility_fxns import GoogleSheetHelper
from app.models import Patient

# from flaskapp.core.ivr_core import *
# from flaskapp.models.ivr_model import *

########################################################################################
# create data each time app starts up (remove db.drop_tables[Patient]) if want to keep data
load_dotenv()
db = connect(os.environ.get('DATABASE_URL'))
db.connect()
db.drop_tables([Patient])
db.create_tables([Patient])

cred_json = "/home/batman/Desktop/flask2heroku/data/key.json"
gsh = GoogleSheetHelper(cred_json, "users_test")

df = gsh.getDataframe("users_test")
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
########################################################################################

@bp.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == "POST":
        Patient.create(
            username=request.form['username']
        )
        db.close()
        return redirect(url_for('main.profile_detail', new_user=request.form['username']))

    users = [user for user in Patient.select()]
    return render_template('index.html', users=users, title="IVR App Demo")

@bp.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with a simple text message."""

    resp = MessagingResponse()
    #msg = resp.message()

    return str(resp)


@bp.route("/profile_detail/<new_user>")
def profile_detail(new_user):
    """ Function for gathering profile information from the Client"""
    #return f"At profile detail for {new_user}"
    return render_template('_new_user.html', new_user=new_user)
    
    #TODO: query from db here in route
    #TODO: set timeszone for user to return proper time from postgres
    # check data in spreadsheet
    # scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    # client = gspread.authorize(creds)
    # spreadsheetName = "Users"
    # sheetName = "Existing"

    # spreadsheet = client.open(spreadsheetName)
    # sheet = spreadsheet.worksheet(sheetName)
    # #all_sheet = sheet.get_all_values()
    # rows = sheet.get_all_records()

    # row_num = 0
    # for r in rows:
    #     ph = r.get('Phone Number')

    #     for v in r:
    #         val = r.get(v)
    #         if val == '':
    #             if v in ('dob', 'gender'):
    #                 print(f'getting {v} from {ph}')
    #                 call_flow('FWa23b5f2570ae23e2e1d68448378af0d0', str(ph))
    #                 break
    #             elif v in ('weight', 'height'):
    #                 print(f'getting {v} from {ph}')
    #                 call_flow ('FW6661af875fa71bfcc36030d653e745ec', str(ph))
    #                 break
    #             elif v in ('activity', 'hobby'):
    #                 print(f'getting {v} from {ph}')
    #                 call_flow('FW8db981daac5317452c78944626de52ac', str(ph))
    #                 break
    #             elif v in ('time zone', 'call time'):
    #                 print(f'getting {v} from {ph}')
    #                 call_flow('FWac7f7be3dcc167fed511d4c08cf76f8c', str(ph))
    #                 break
    #             elif v in ('emergency phone', 'emergency name'):
    #                 print(f'getting {v} from {ph}')
    #                 call_flow('FW21a0b56a4c5d0d9635f9f86616036b9c', str(ph))
    #                 break
    #         else:
    #             print(f'for {ph}:{v} is good')


# def voice_joined():
#     """ Function for making joined call """
#     resp = VoiceResponse()
#     tel = request.form['From']
#     answer = request.form['SpeechResult']
#     if 'Yes' in answer:
#         save_new_user(tel, 'Existing')
#         resp.say('Thanks for joining us. \n'
#                  'We are glad to welcome you to our social network. \n'
#                  'Heart Voices is a unique platform where you can make friends with the same interests.\n'
#                  'With us, you can use Google search through your phone. \n'
#                  'You can take advantage of the unique smart reminder feature. \n'
#                  'Our system will remind you every day of important events for you, it can be a daily medication intake, the need to do something, or a reminder that you really want to learn a new language.\n'
#                  'At your request, we will remind you to measure blood pressure or blood sugar, and we will collect this data for you. You can use them when you visit your doctor if needed. \n'
#                  'We provide social support through friendly calls to friends and our operators. \n'
#                  'After forwarding call you will access to our community.')
#         resp.dial(optional_number)
#     else:
#         resp.say(f'We got your answer {answer}. We hope you will back us later. Take care.')
#         resp.hangup()
#     return(str(resp))

# def voice():
#     """ Function for answering from any call to Main Number of the IVR """
#     resp = VoiceResponse()
#     tel = request.values['From']
#     user = check_new_user(tel)
#     if user == 'Exist':resp.dial(optional_number)
#     else:
#         save_new_user(tel,'Calls')
#         gather = Gather(input='speech dtmf', action='/voice_joined',  timeout=3, num_digits=1)
#         gather.say('Welcome to Heart Voices ! We are really helping to people in their journey to a healthy life. Do you want to join us? Say yes or no.')
#         resp.append(gather)
#     return str(resp)



# def after_call():
#     """ Function for saving data after call to spreadsheet """
#     resp = VoiceResponse()
#     req = request.values
#     for r in req:
#         save_data(r, req.get(r), req.get('phone'))
#     return str(resp)

# def username():
#     """ Function for getting Name of the Client from google spreadsheet """
#     req = request.values
#     phone = req.get('phone')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     all_sheet = sheet.get_all_values()
#     rows = sheet.get_all_records()
#     x = {}
#     for row in rows:
#         tel = row.get('Phone Number')
#         if phone == f'+{tel}':
#             x = {"username": row.get('username')}
#     return (jsonify(x))

# def check_client_type():
#     """ Function for checking Type of the Client from google spreadsheet (Client, Volunteer,Client and Volunteer, QA Engineer """
#     req = request.values
#     phone = req.get('phone')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     all_sheet = sheet.get_all_values()
#     rows = sheet.get_all_records()
#     x = {}
#     for row in rows:
#         tel = row.get('Phone Number')
#         if phone == f'+{tel}':
#             x = {"type": row.get('type')}
#     return (jsonify(x))

# def save_client_type():
#     """ Function for checking Type of the Client from google spreadsheet (Client, Volunteer,Client and Volunteer, QA Engineer """
#     resp = VoiceResponse()
#     req = request.values
#     save_data('type', req.get('client_type'), req.get('phone'))
#     return str(resp)


# def call_to_friend():
#     """ Function for making call to the friend according data in the spreadsheet """
#     resp = VoiceResponse()

#     req = request.values
#     phone = req.get('phone')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     rows = sheet.get_all_records()
#     x = {}
#     for row in rows:
#         tel = row.get('Phone Number')
#         if phone == f'+{tel}':
#             x = {f"friend": row.get('friend')}
#     return (jsonify(x))


# def find_friend_timezone():
#     """Selects a match from Google sheet and connects User to friend"""
#     # Start our TwiML response
#     resp = VoiceResponse()
#     to_number = request.form['To']
#     from_number = request.form['From']  #tel = request.values['From']
    
#     # timezone helper class to get time zone from number
#     tz_from = TimeZoneHelper(from_number)

#     # how to get match from temporary google sheet
#     dataframe = getTemporaryUserData()
#     match = matchFromDf(dataframe, tz_from)

#     # now that we have match, forward call to match
#     formatMatch = "+" + str(match)
#     resp.say(
#         "Connecting you to a friend. Please stay on the line."
#     )
#     resp.dial(formatMatch, action=url_for('.end_call')) # requires "action" route to be routed to when call ends
#     return Response(str(resp), 200, mimetype="application/xml")

# def end_call():
#     """Thank user & hang up."""
#     response = VoiceResponse()
#     response.say(
#         "Thank you for using the Heart Voices IVR System! " + "Your voice makes a difference. Goodbye."
#     )
#     response.hangup()
#     return Response(str(response), 200, mimetype="application/xml")


# def call_to_operator():
#     """ Function for making call to the operator according data in the spreadsheet """
#     resp = VoiceResponse()

#     req = request.values
#     phone = req.get('phone')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     rows = sheet.get_all_records()
#     x = {}
#     for row in rows:
#         tel = row.get('Phone Number')
#         if phone == f'+{tel}':
#             x = {'operator': row.get('operator')}
#     return (jsonify(x))

# def save_blood_pressure():
#     """ Function for saving measurement of the blood pressure to the spreadsheet """
#     resp = VoiceResponse()

#     req = request.values
#     phone = req.get('phone')
#     UP = ''.join(e for e in req.get('UP') if e.isalnum())
#     DOWN = ''.join(e for e in req.get('DOWN') if e.isalnum())

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)
#     spreadsheetName = "health_metrics"
#     sheetName = "blood_pressure"
#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     new_row = [phone, UP, DOWN, json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)]
#     sheet.append_row(new_row)

#     return(str(resp))

# def save_feedback_service():
#     """ Function for gathering feedback and put information about it to google spreadsheet """
#     resp = VoiceResponse()
#     req = request.values

#     phone = ''
#     REurl = 'YES'
#     if req.get('phone'):
#         phone = req.get('phone')
#     else:
#         account_sid = os.environ['TWILIO_ACCOUNT_SID']
#         auth_token = os.environ['TWILIO_AUTH_TOKEN']
#         client = Client(account_sid, auth_token)
#         call = client.calls(req.get('CallSid')).fetch()
#         phone = call.from_
#         REurl = req.get('RecordingUrl')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)
#     spreadsheetName = "feedback"
#     sheetName = "service"
#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), phone, REurl]
#     sheet.append_row(new_row)
#     send_mail("FEEDBACK", phone=phone, feedback=REurl)

#     return (str(resp))
# def save_feedback():
#     """ Function for saving feedback and to the google spreadsheet """
#     try:
#         # GET username from SPREDASHEET
#         phone = request.args.get('phone')
#         msg = request.args.get('msg')
#         scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#         creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#         client = gspread.authorize(creds)
#         spreadsheetName = "feedback"
#         sheetName = "service"
#         spreadsheet = client.open(spreadsheetName)
#         sheet = spreadsheet.worksheet(sheetName)

#         new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), phone, msg]
#         sheet.append_row(new_row)
#         send_mail("FEEDBACK", phone=phone, feedback=msg)
#     except:
#         return('-1')
#     return ('0')


# def search():
#     """ Function for answering search results on phrase from Client"""
#     req = request.values
#     req_str = req.get('str')

#     results = google_search(req_str, my_api_key, my_cse_id, num=10)
#     it = 0
#     str = ''
#     for result in results:
#         #title=result.get('title')
#         res=result.get('snippet')
#         #name = result.get('displayLink')
#         str= str + f'{lst_num[it]} result: {res}".\n'
#         it=it+1
#         if it == 3: break
#     x = {"search_result": str}
#     return (jsonify(x))

# def get_next_reminder():
#     req = request.values
#     phone = req.get('phone')
#     tel = str(phone[1:15]) # exclude +

#     #conn.connect()
#     # get Patient ID by the phone
#     pat = Patient.get(Patient.phone == tel)
#     print(pat.id, pat.phone)

#     # get SmartReminders by Patient ID
#     #smr = SmartReminder.get(SmartReminder.id==pat.id)
#     query = SmartReminder.select().where(SmartReminder.patient_id == pat.id).order_by(SmartReminder.next_time).limit(1)
#     smr_selected = query.dicts().execute()

#     result = ''
#     # get reminder text by SmartReminder ID
#     for s in smr_selected:
#         rm = Reminder.get(Reminder.id==s['reminder_id'])
#         result = rm.text
#         print (rm.text)
#         # change next time of reminding
#         update_reminder(s['reminder_id'])
#         conn.commit()
#     conn.close()
#     x = {"text":f' Lets listen interesting fact of the day...{result} ...Thank you.'}
#     return (jsonify(x))



# def voice_joined():
#     """ Function for making joined call """
#     resp = VoiceResponse()
#     tel = request.form['From']
#     answer = request.form['SpeechResult']
#     if 'Yes' in answer:
#         save_new_user(tel, 'Existing')
#         resp.say('Thanks for joining us. \n'
#                  'We are glad to welcome you to our social network. \n'
#                  'Heart Voices is a unique platform where you can make friends with the same interests.\n'
#                  'With us, you can use Google search through your phone. \n'
#                  'You can take advantage of the unique smart reminder feature. \n'
#                  'Our system will remind you every day of important events for you, it can be a daily medication intake, the need to do something, or a reminder that you really want to learn a new language.\n'
#                  'At your request, we will remind you to measure blood pressure or blood sugar, and we will collect this data for you. You can use them when you visit your doctor if needed. \n'
#                  'We provide social support through friendly calls to friends and our operators. \n'
#                  'After forwarding call you will access to our community.')
#         resp.dial(optional_number)
#     else:
#         resp.say(f'We got your answer {answer}. We hope you will back us later. Take care.')
#         resp.hangup()
#     return(str(resp))

# def voice():
#     """ Function for answering from any call to Main Number of the IVR """
#     resp = VoiceResponse()
#     tel = request.values['From']
#     user = check_new_user(tel)
#     if user == 'Exist':resp.dial(optional_number)
#     else:
#         save_new_user(tel,'Calls')
#         gather = Gather(input='speech dtmf', action='/voice_joined',  timeout=3, num_digits=1)
#         gather.say('Welcome to Heart Voices ! We are really helping to people in their journey to a healthy life. Do you want to join us? Say yes or no.')
#         resp.append(gather)
#     return str(resp)



# def after_call():
#     """ Function for saving data after call to spreadsheet """
#     resp = VoiceResponse()
#     req = request.values
#     for r in req:
#         save_data(r, req.get(r), req.get('phone'))
#     return str(resp)

# def username():
#     """ Function for getting Name of the Client from google spreadsheet """
#     req = request.values
#     phone = req.get('phone')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     all_sheet = sheet.get_all_values()
#     rows = sheet.get_all_records()
#     x = {}
#     for row in rows:
#         tel = row.get('Phone Number')
#         if phone == f'+{tel}':
#             x = {"username": row.get('username')}
#     return (jsonify(x))

# def check_client_type():
#     """ Function for checking Type of the Client from google spreadsheet (Client, Volunteer,Client and Volunteer, QA Engineer """
#     req = request.values
#     phone = req.get('phone')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     all_sheet = sheet.get_all_values()
#     rows = sheet.get_all_records()
#     x = {}
#     for row in rows:
#         tel = row.get('Phone Number')
#         if phone == f'+{tel}':
#             x = {"type": row.get('type')}
#     return (jsonify(x))

# def save_client_type():
#     """ Function for checking Type of the Client from google spreadsheet (Client, Volunteer,Client and Volunteer, QA Engineer """
#     resp = VoiceResponse()
#     req = request.values
#     save_data('type', req.get('client_type'), req.get('phone'))
#     return str(resp)


# def call_to_friend():
#     """ Function for making call to the friend according data in the spreadsheet """
#     resp = VoiceResponse()

#     req = request.values
#     phone = req.get('phone')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     rows = sheet.get_all_records()
#     x = {}
#     for row in rows:
#         tel = row.get('Phone Number')
#         if phone == f'+{tel}':
#             x = {f"friend": row.get('friend')}
#     return (jsonify(x))


# def find_friend_timezone():
#     """Selects a match from Google sheet and connects User to friend"""
#     # Start our TwiML response
#     resp = VoiceResponse()
#     to_number = request.form['To']
#     from_number = request.form['From']  #tel = request.values['From']
    
#     # timezone helper class to get time zone from number
#     tz_from = TimeZoneHelper(from_number)

#     # how to get match from temporary google sheet
#     dataframe = getTemporaryUserData()
#     match = matchFromDf(dataframe, tz_from)

#     # now that we have match, forward call to match
#     formatMatch = "+" + str(match)
#     resp.say(
#         "Connecting you to a friend. Please stay on the line."
#     )
#     resp.dial(formatMatch, action=url_for('.end_call')) # requires "action" route to be routed to when call ends
#     return Response(str(resp), 200, mimetype="application/xml")

# def end_call():
#     """Thank user & hang up."""
#     response = VoiceResponse()
#     response.say(
#         "Thank you for using the Heart Voices IVR System! " + "Your voice makes a difference. Goodbye."
#     )
#     response.hangup()
#     return Response(str(response), 200, mimetype="application/xml")


# def call_to_operator():
#     """ Function for making call to the operator according data in the spreadsheet """
#     resp = VoiceResponse()

#     req = request.values
#     phone = req.get('phone')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     rows = sheet.get_all_records()
#     x = {}
#     for row in rows:
#         tel = row.get('Phone Number')
#         if phone == f'+{tel}':
#             x = {'operator': row.get('operator')}
#     return (jsonify(x))

# def save_blood_pressure():
#     """ Function for saving measurement of the blood pressure to the spreadsheet """
#     resp = VoiceResponse()

#     req = request.values
#     phone = req.get('phone')
#     UP = ''.join(e for e in req.get('UP') if e.isalnum())
#     DOWN = ''.join(e for e in req.get('DOWN') if e.isalnum())

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)
#     spreadsheetName = "health_metrics"
#     sheetName = "blood_pressure"
#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     new_row = [phone, UP, DOWN, json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)]
#     sheet.append_row(new_row)

#     return(str(resp))

# def save_feedback_service():
#     """ Function for gathering feedback and put information about it to google spreadsheet """
#     resp = VoiceResponse()
#     req = request.values

#     phone = ''
#     REurl = 'YES'
#     if req.get('phone'):
#         phone = req.get('phone')
#     else:
#         account_sid = os.environ['TWILIO_ACCOUNT_SID']
#         auth_token = os.environ['TWILIO_AUTH_TOKEN']
#         client = Client(account_sid, auth_token)
#         call = client.calls(req.get('CallSid')).fetch()
#         phone = call.from_
#         REurl = req.get('RecordingUrl')

#     # GET username from SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)
#     spreadsheetName = "feedback"
#     sheetName = "service"
#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), phone, REurl]
#     sheet.append_row(new_row)
#     send_mail("FEEDBACK", phone=phone, feedback=REurl)

#     return (str(resp))
# def save_feedback():
#     """ Function for saving feedback and to the google spreadsheet """
#     try:
#         # GET username from SPREDASHEET
#         phone = request.args.get('phone')
#         msg = request.args.get('msg')
#         scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#         creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#         client = gspread.authorize(creds)
#         spreadsheetName = "feedback"
#         sheetName = "service"
#         spreadsheet = client.open(spreadsheetName)
#         sheet = spreadsheet.worksheet(sheetName)

#         new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), phone, msg]
#         sheet.append_row(new_row)
#         send_mail("FEEDBACK", phone=phone, feedback=msg)
#     except:
#         return('-1')
#     return ('0')


# def search():
#     """ Function for answering search results on phrase from Client"""
#     req = request.values
#     req_str = req.get('str')

#     results = google_search(req_str, my_api_key, my_cse_id, num=10)
#     it = 0
#     str = ''
#     for result in results:
#         #title=result.get('title')
#         res=result.get('snippet')
#         #name = result.get('displayLink')
#         str= str + f'{lst_num[it]} result: {res}".\n'
#         it=it+1
#         if it == 3: break
#     x = {"search_result": str}
#     return (jsonify(x))

# def get_next_reminder():
#     req = request.values
#     phone = req.get('phone')
#     tel = str(phone[1:15]) # exclude +

#     #conn.connect()
#     # get Patient ID by the phone
#     pat = Patient.get(Patient.phone == tel)
#     print(pat.id, pat.phone)

#     # get SmartReminders by Patient ID
#     #smr = SmartReminder.get(SmartReminder.id==pat.id)
#     query = SmartReminder.select().where(SmartReminder.patient_id == pat.id).order_by(SmartReminder.next_time).limit(1)
#     smr_selected = query.dicts().execute()

#     result = ''
#     # get reminder text by SmartReminder ID
#     for s in smr_selected:
#         rm = Reminder.get(Reminder.id==s['reminder_id'])
#         result = rm.text
#         print (rm.text)
#         # change next time of reminding
#         update_reminder(s['reminder_id'])
#         conn.commit()
#     conn.close()
#     x = {"text":f' Lets listen interesting fact of the day...{result} ...Thank you.'}
#     return (jsonify(x))
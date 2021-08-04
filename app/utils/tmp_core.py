from oauth2client.service_account import ServiceAccountCredentials
from supermemo2 import SMTwo
import gspread
import time
import datetime
import json
from twilio.rest import Client as Client
import os
# from googleapiclient.discovery import build
# from flaskapp.settings import *
# from flaskapp.tools.util import *
# from flaskapp.models.ivr_model import *


# # def out_bound_call (tel):
# #     """ Function for making outbound call"""
# #     account_sid = os.environ['TWILIO_ACCOUNT_SID']
# #     auth_token = os.environ['TWILIO_AUTH_TOKEN']
# #     client = Client(account_sid, auth_token)
# #     status = check_new_user(tel)
# #     if (status != 'New'):
# #         execution = client.studio \
# #             .flows('FW66222e22d7301b1f1e0f02ca198c440a') \
# #             .executions \
# #             .create(to=tel, from_=main_number)
# #     else:
# #         execution = client.studio \
# #             .flows('FW21a0b56a4c5d0d9635f9f86616036b9c') \
# #             .executions \
# #             .create(to=tel, from_=main_number)
# # def call_flow(flow_sid, tel=''):
# #     """ Function for calling any flow from Twilio Studion """
# #     account_sid = os.environ['TWILIO_ACCOUNT_SID']
# #     auth_token = os.environ['TWILIO_AUTH_TOKEN']
# #     client = Client(account_sid, auth_token)
# #     if tel != '':
# #         status = check_new_user(tel)
# #         if (status != 'New'):
# #             print (f'start call for existing User {tel}')
# #             execution = client.studio \
# #                 .flows(flow_sid) \
# #                 .executions \
# #                 .create(to=tel, from_=main_number)
# #             # wait for getting data from studio flow
# #             steps = client.studio.flows(flow_sid) \
# #                 .executions(execution.sid) \
# #                 .steps \
# #                 .list(limit=20)
# #         else:
# #             print(f'start call for new User {tel}')
# #             execution = client.studio \
# #                 .flows('FW66222e22d7301b1f1e0f02ca198c440a') \
# #                 .executions \
# #                 .create(to=tel, from_=main_number)


# #             # while len(steps) < 12:
# #             #     steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
# #             #         .executions(execution.sid) \
# #             #         .steps \
# #             #         .list(limit=20)
# #             #     time.sleep(5)
# #             #     print(len(steps))
# #             #
# #             # last_step_sid = steps[0].sid
# #             # execution_step_context = client.studio \
# #             #     .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
# #             #     .executions(execution.sid) \
# #             #     .steps(last_step_sid) \
# #             #     .step_context() \
# #             #     .fetch()
def profile_detail():
    """ Function for gathering profile information from the Client"""
    # check data in spreadsheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)
    spreadsheetName = "Users"
    sheetName = "Existing"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)
    #all_sheet = sheet.get_all_values()
    rows = sheet.get_all_records()

    row_num = 0
    for r in rows:
        ph = r.get('Phone Number')

        for v in r:
            val = r.get(v)
            if val == '':
                if v in ('dob', 'gender'):
                    print(f'getting {v} from {ph}')
                    call_flow('FWa23b5f2570ae23e2e1d68448378af0d0', str(ph))
                    break
                elif v in ('weight', 'height'):
                    print(f'getting {v} from {ph}')
                    call_flow ('FW6661af875fa71bfcc36030d653e745ec', str(ph))
                    break
                elif v in ('activity', 'hobby'):
                    print(f'getting {v} from {ph}')
                    call_flow('FW8db981daac5317452c78944626de52ac', str(ph))
                    break
                elif v in ('time zone', 'call time'):
                    print(f'getting {v} from {ph}')
                    call_flow('FWac7f7be3dcc167fed511d4c08cf76f8c', str(ph))
                    break
                elif v in ('emergency phone', 'emergency name'):
                    print(f'getting {v} from {ph}')
                    call_flow('FW21a0b56a4c5d0d9635f9f86616036b9c', str(ph))
                    break
            else:
                print(f'for {ph}:{v} is good')

def call_to_check_bld():
    """ Function for checking blood pressure and saving results to google spreadsheet """
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    # call studio flow from Python app

    execution = client.studio \
        .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions \
        .create(to='+16692419870', from_=main_number)

    steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions(execution.sid) \
        .steps \
        .list(limit=20)
    while len(steps) < 12:
        steps = client.studio.flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
            .executions(execution.sid) \
            .steps \
            .list(limit=20)
        time.sleep(5)
        print(len(steps))
    # sid = execution.sid
    # execution_step = client.studio \
    #                         .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
    #                         .executions('FN76531ee7fcda3617d99bec690d915045') \
    #                         .steps \
    #                         .fetch()

    # call specific Flow and Execution only for understanding and deveopment
    # execution = client.studio \
    #                   .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
    #                   .executions('FN76531ee7fcda3617d99bec690d915045') \
    #                   .fetch()

    last_step_sid = steps[0].sid
    execution_step_context = client.studio \
        .flows('FWfb6357ea0756af8d65bc2fe4523cb21a') \
        .executions(execution.sid) \
        .steps(last_step_sid) \
        .step_context() \
        .fetch()

    UP = execution_step_context.context['flow']['variables'].get('UP')
    DOWN = execution_step_context.context['flow']['variables'].get('DOWN')

    # PUT DATA TO SPREDASHEET
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
    client = gspread.authorize(creds)

    new_row = [json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), UP, DOWN]
    spreadsheetName = "Ekaterina"
    sheetName = "Blood_Preassure"

    spreadsheet = client.open(spreadsheetName)
    sheet = spreadsheet.worksheet(sheetName)

    sheet.append_row(new_row)
    time.sleep(5)
# def check_new_user(tel=''):
#     """ Function for checking type of User (NEW/EXISTING) """
#     # check data in spreadsheet
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)
#     all_sheet = sheet.get_all_values()
#     phone_lst = []
#     for a in all_sheet:phone_lst.append(a[0])
#     tel_not_plus = str(tel[1:15])
#     if tel_not_plus in phone_lst:
#         return 'Exist'
#     else:
#         return 'New'


# def save_new_user(tel='', tab=''):
#     """ Function for saving NEW user in google spreadsheet"""
#     # check data in spreadsheet
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = 'Users'
#     sheetName = tab

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     new_row = [tel[1:15],'','','','','','','','','','','',json.dumps(datetime.datetime.now(),indent=4, sort_keys=True, default=str),'19258609793','19258609793']
#     sheet.append_row(new_row)
#     send_mail("NEW USER", phone=tel)

# def save_data(col_name, value, tel):
#     """ Function for saving data to google spreadsheet """
#     # PUT DATA TO SPREDASHEET
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scope)
#     client = gspread.authorize(creds)

#     spreadsheetName = "Users"
#     sheetName = "Existing"

#     spreadsheet = client.open(spreadsheetName)
#     sheet = spreadsheet.worksheet(sheetName)

#     all_sheet = sheet.get_all_values()
#     rows = sheet.get_all_records()
#     row_num = 0
#     for r in all_sheet:
#         row_num = row_num + 1
#         ph = r[0] #find the Phone Number
#         if tel == f'+{ph}':
#             break

#     col_num = 0
#     for c in all_sheet[0]:
#         col_num = col_num + 1
#         if col_name == c:
#             print(row_num, col_num, col_name, value)
#             sheet.update_cell(row_num, col_num, value)
#             break

# def google_search(search_term, api_key, cse_id, **kwargs):
#     """ Function for using Google Search API"""
#     service = build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
#     return res['items']
# # def print_mars_photos():
# #     from redis import Redis
# #     from rq import Queue
# #
# #     from mars import get_mars_photo
# #
# #     q = Queue(connection=Redis())
# #
# #     print('Before')
# #     for i in range(10):
# #         #get_mars_photo(1 + i)
# #         q.enqueue(get_mars_photo, 1 + i)
# #     print('After')
# #print_mars_photos()


# def update_reminder(id):

#     # get smart reminder by ID
#     smr = SmartReminder.get(SmartReminder.id==id)
#     #smr = SmartReminder()
#     r = SMTwo.first_review(3)
#     if smr.last_time is None:
#         # first review
#         r = SMTwo.first_review(3)
#         print(r)
#     else:
#         # next review
#         r = SMTwo(smr.easiness, smr.interval, smr.repetitions).review(3)
#         print(r)
#     smr.interval = r.interval
#     smr.easiness = r.easiness
#     smr.repetitions = r.repetitions
#     smr.last_time = datetime.datetime.now()
#     smr.next_time = r.review_date
#     smr.save()
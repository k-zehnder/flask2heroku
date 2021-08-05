from datetime import datetime
from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.models import Patient
from app.main import bp

from app.utils.tmp_core import call_to_check_bld


@bp.route('/')
def hello():
    return "Hello World!"

@bp.route("/profile_detail")
def profile_detail():
    """ Function for gathering profile information from the Client"""
    return "At profile detail"

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


@bp.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with a simple text message."""

    resp = MessagingResponse()
    #msg = resp.message()

    return str(resp)




from flask import render_template, redirect, url_for, flash, request, abort
from app.models import Patient
from app import db
from app.auth import bp

# from flaskapp.tools.authtools import send_otp, verify_otp
from app.utils.authtools import send_otp, verify_otp

@bp.route("/get_otp")
def get_otp():
    '''Ph number should be a string in format +<country code><number>'''
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not len(data) == 1 and not 'phone' in data:
                msg = f'Incorrect data format'
                abort(400,msg)
            if send_otp(to = data.get('phone')):
                return {"message":"success",'exit_code':0}
        except RuntimeError as e:
            return {'message':'failed','exit_code':'1','status_code':501,'error':str(e)}
        except ConnectionError as e:
            abort(500,e)

@bp.route("/validate_otp")
def validate_otp():
    '''otp and phone number should be a string'''
    if request.method == "POST":
        data = request.get_json()
        if 'phone' in data and 'otp' in data and len(data) == 2:
            if verify_otp(otp = data.get('otp'),ph = data.get('phone')):
                return {"message":"success",'exit_code':0}
            else:
                abort(403,'Invalid OTP or Validation failed ')
        else:
            abort(400)
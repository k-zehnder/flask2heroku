from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Patient
# from .forms import ContactForm, LoginForm
# # from app.utils import send_mail
from app.main import bp

@bp.route('/')
def hello():
    return "Hello World!"


@bp.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)
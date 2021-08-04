from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.models import Patient
from app.main import bp

@bp.route('/')
def hello():
    return "Hello World!"

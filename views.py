from flask import render_template, flash, url_for, request, redirect
from flask_security.utils import encrypt_password
from flask_security import roles_accepted, roles_required
from flask_admin import Admin, AdminIndexView
from flask_login import login_required
from app import app
from models import *
import os

"""
    This is to create tables and models in the database.
"""
@app.before_first_request
def before_first_request():
    db.create_all
    db.session.commit

@app.route('/')
def home():
    return render_template('index.html')
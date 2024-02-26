from flask import render_template, request, flash, jsonify, send_file, redirect
from sqlalchemy import desc
from .. import app, db
import json
import re
from ..const import *
from ..models import *
from ..user import *

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    user = User('dvandyuk')
    login_user(user)
    return redirect('/')
 
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')   
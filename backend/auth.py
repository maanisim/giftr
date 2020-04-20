from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form('email')
    password = request.form('passw')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user exists
    # check if credentials is wrong
    if not user or not check_password_hash(user.password, password):
        return render_template(url_for('auth.login'))

    # if credentials are right    
    return redirect(url_for('main.profile'))
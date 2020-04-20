from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/loginapi', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
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
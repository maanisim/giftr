from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    email = request.form.get('email')
    password = request.form.get('passw')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user exists
    # check if credentials is wrong
    if not user or not check_password_hash(user.password, password):
        return render_template(url_for('auth.login'))

    # if credentials are right    
    return redirect(url_for('main.profile'))

@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    password = request.form.get('passw')
    username = request.form.get('name')

    user = User.query.filter_by(email=email).first()
    if user: # if a user is found with the email used
        return redirect(url_for('auth.signup'))

    new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
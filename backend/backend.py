from flask import Flask, redirect, url_for, render_template, request, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, login_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import re, hashlib, os

# INIT
app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://web:AN(G3hg93hgn2ffim@localhost/dummy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), primary_key=False, unique=False, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# ----------------- ROUTES -----------------
@app.route('/login-post', methods=['POST'])
def login_post():
    email = request.form('email')
    password = request.form('passw')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user exists
    # check if credentials is wrong
    if not user or not check_password_hash(user.password, password):
        return render_template(url_for('login'))

    # if credentials are right    
    login_user(user, remember=remember)
    return redirect(url_for('index'))

@app.route('/register-post', methods=['POST'])
def register_post():
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('my_profile.html',
        username=session['username'])
    return redirect(url_for('index'))

@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    print("welcome")
    if 'loggedin' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

# ----------------- STATIC ROUTES -----------------
@app.route('/item')
def item():
    return render_template('itemPage.html')

@app.route('/anotherProfile')
def anotherProfile():
    return render_template('anotherProfile.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/contact')
def contact():
    return render_template('contact.php')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/suggestion')
def suggestion():
    return render_template('suggestion.html')

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()

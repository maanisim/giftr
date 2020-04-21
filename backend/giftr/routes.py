from giftr import app, mysql
from flask import Flask, redirect, url_for, render_template, request, session, make_response
from flask_mysqldb import MySQLdb
import ssl, hashlib, re, datetime, smtplib
from math import floor as floor

global COOKIE_TIME_OUT
COOKIE_TIME_OUT = 60*60*24*7  # 7 days

app.errorhandler(404)


def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/')
def index():
    if 'loggedin' in session:
        # Already logged in
        # You can tell you are logged in by register/login disappering on the right and being replaced with "my profile"
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

# -------------------------------------------------- AUTH ROUTES --------------------------------------------------


@app.route('/login', methods=['POST', 'GET'])
def login():
    # LOGGING IN
    if not 'loggedin' in session and request.method == 'POST' and 'email' in request.form and 'passw' in request.form:
        email = request.form['email']
        # hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()
        password = request.form['passw']

        # Check if account exists in DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        # Fetch account
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['email'] = account['email']
            session['username'] = account['username']
            session['gender'] = account['gender']
            session['age'] = account['age']
            remember = request.form.getlist('remember')

            if remember:
                resp = make_response(redirect('/'))
                resp.set_cookie('email', email, max_age=COOKIE_TIME_OUT)
                #resp.set_cookie('password', password, max_age=COOKIE_TIME_OUT)
                resp.set_cookie('rem', 'checked', max_age=COOKIE_TIME_OUT)
                return resp
            return redirect('/')
        else:
            msg = 'Incorrect login details!'
            return render_template('login.html')
    elif not 'loggedin' in session:
        return render_template('login.html')
    elif 'loggedin' in session:
        return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    # CREATING ACCOUNT
    if not 'loggedin' in session and request.method == 'POST' and 'name' in request.form and 'passw' in request.form and 'email' in request.form:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist
        # Create variables for easy access
        username = request.form['name']
        password = hashlib.sha256(
            request.form['passw'].encode('utf-8')).hexdigest()
        email = request.form['email']
        bdaymonth = request.form['bdaymonth']
        bdaymonth = bdaymonth.split('-')
        age = floor(int((((datetime.datetime.now().year - int(bdaymonth[0])) * 12) + int(bdaymonth[1]))/12))
        gender = "Male"
        token = "TEST"
        photo = "blank.jpg"

        # Check if account exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        # Fetch account
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO users (username, password, token, email, name, age, gender, photo)'
                           'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (username, password, token, email, username, age, gender, photo))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('welcome'))
    elif not 'loggedin' in session:
        return render_template('login.html')
    elif 'loggedin' in session:
        return render_template('index.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('email', None)
        return redirect('/')
    return redirect('/')


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('my_profile.html', username=session['username'])
    return redirect('/')

# test
@app.route('/search', methods=['POST', 'GET'])
def search():
    if(request.method == 'POST' and 'search' in request.form):
        search = request.form['search']
        if(re.match("^[A-Za-z0-9_-]*$", search) is not None):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT products.name FROM products WHERE products.name LIKE \'%'+search+'%\' LIMIT 5')
            row = cursor.fetchone()
            while row is not None:
                print(str(row))
                row = cursor.fetchone()
    return render_template('search.html')


@app.route('/emailSent', methods=['POST', 'GET'])
def emailsent():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        message = """\
            {}
        Subject: From {}
        {}""".format(email, name, message)

        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "group16uol@gmail.com"  # Enter your address
        receiver_email = "group16uol@gmail.com"  # Enter receiver address
        password = "Tataract52"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    return render_template('emailSent.html')


@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    print("welcome")
    if 'loggedin' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return render_template('index.html')


@app.route('/new_settings')
def new_settings():
    if 'loggedin' in session:
        if(request.method['email'] == request.method['confirmEmail'] and request.method['passw'] == request.method['cofirmPassw']):
            email = request.method['email']
            password = request.method['passw']
            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
                if not re.match(r"(^[a-zA-Z0-9_.+-]^$)", password):
                    print(email)
                    print(password)
    return render_template('404.html')

# -------------------------------------------------- STATIC ROUTES --------------------------------------------------


@app.route('/settings')
def settings():
    if 'loggedin' in session:
        return render_template('settings.html')
    return render_template('404.html')


@app.route('/questionnaire')
def questionnaire():
    if 'loggedin' in session:
        return render_template('index.html')
    return render_template('404.html')


@app.route('/forgot')
def forgot():
    if 'loggedin' in session:
        return render_template('index.html')
    return render_template('forgotPsw.html')


@app.route('/friend')
def friend():
    if 'loggedin' in session:
        return render_template('anotherProfile.html')
    return render_template('404.html')


@app.route('/item')
def item():
    return render_template('itemPage.html')


@app.route('/wishlist')
def wishlist():
    if 'loggedin' in session:
        return render_template('wishlist.html')
    return render_template('404.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/suggestion')
def suggestion():
    return render_template('suggestion.html')

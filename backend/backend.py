# Really basic program for now
from flask import Flask, redirect, url_for, render_template, request, session, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re, hashlib, os
from _datetime import timedelta
import smtplib, ssl

app = Flask(__name__, )
app.secret_key = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

# DB Connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'web'
app.config['MYSQL_PASSWORD'] = 'AN(G3hg93hgn2ffim'
app.config['MYSQL_DB'] = 'dummy'

# Initialise DB
mysql = MySQL(app)

global COOKIE_TIME_OUT
COOKIE_TIME_OUT = 60*60*24*7 # 7 days

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('my_profile.html',
        username=session['username'])
    return redirect('/')

@app.route('/')
def index():
    if 'loggedin' in session:
        # Already logged in
        #You can tell you are logged in by register/login disappering on the right and being replaced with "my profile"
        return render_template('index.html', username=session['username']) 
    return render_template('index.html')

# mostly static pages
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
    return render_template('contact.html')

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

@app.route('/loginapi', methods=['POST', 'GET'])
def loginapi():
    #LOGGING IN
    if request.method == 'POST' and 'email' in request.form and 'passw' in request.form:
        email = request.form['email']
        password = request.form['passw'] # hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()

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

#check if user length min 8
#check if password length min 8
#check if user = a-zA-Z0-9
#check if password = a-zA-Z0-9
#check if username used in db else error
#check if email used in db else error
#add to database
@app.route('/registerapi', methods=['POST', 'GET'])
def registerapi():
    #CREATING ACCOUNT
    if request.method == 'POST' and 'username' in request.form and 'passw' in request.form and 'email' in request.form:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist
        if request.method == 'POST' and 'username' in request.form and 'passw' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['name']
            password = hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()
            email = request.form['email']

        # Check if account exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        # Fetch account
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('welcome'))        
    return render_template('register.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('email', None)
        return redirect('/')
    return redirect('/')


@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    print("welcome")
    if 'loggedin' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()

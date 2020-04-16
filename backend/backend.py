# Really basic program for now
from flask import Flask, redirect, url_for, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, re, hashlib
app = Flask(__name__)

#DB Connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'web'
app.config['MYSQL_PASSWORD'] = 'AN(G3hg93hgn2ffim'
app.config['MYSQL_DB'] = 'dummy'

# Initialise DB
mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'passw' in request.form:
        email = request.form['email']
        password = hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()
        # Check if account exists in DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s',(email, password))
        # Fetch account
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['email'] = account['email']
            return redirect(url_for('home'))            
    else:
        msg = 'Incorrect login details!'
        return render_template('login.html')
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''

    # Check if "username", "password" and "email" POST requests exist
    if request.method == 'POST' and 'username' in request.form and 'passw' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()
        email = request.form['email']

    # Check if account exists
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s',(email, password))
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


@app.route('/api/logout', methods=['POST', 'GET'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)


@app.route('/api/home', methods=['POST', 'GET'])
def home():
    if 'loggedin' in session:
        #Logged in
        return render_template('home.html', email=session['email'])
    return render_template('index.html')


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
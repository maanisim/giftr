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


@app.route('/api', methods=['POST', 'GET'], host="giftr.cf:443")
def login():
    if request.method == 'POST' and 'email' in request.form and 'passw' in request.form:
        email = request.form['email']
        password = request.form['passw'] #hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()
        # Check if account exists in DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s',(email, password))
        # Fetch account
        account = cursor.fetchone()
        return redirect(url_for("user", usr=email))

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            return redirect(url_for('home'))            
    else:
        msg = 'Incorect login details!'
        return render_template("backTest.html")

    return render_template('index.html', msg=msg)


@app.route('/api', methods=['POST', 'GET'], host="giftr.cf:443")
def register():
    if request.method == 'POST' and 'name' in request.form and 'passw' in request.form and 'email' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['passw']


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)


@app.route('/home')
def home():
    if 'loggedin' in session:
        #Logged in
        return render_template('home.html', user=session['email'])
    return redirect(url_for('login'))


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host= 'giftr.cf:443')
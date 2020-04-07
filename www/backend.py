# Really basic program for now
#
#
from flask import Flask, redirect, url_for, render_template, request, session
from flask_mysqldb import MYSQL
import MySQLdb.cursors
import re
app = Flask(__name__)

# DB Connection details
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''

# Initialise DB
mysql = MYSQL(app)

@app.route('/')
def home():
    return render_template("backTest.html")


@app.route('/api', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'passw' in request.form:
        email = request.form['email']
        password = request.form['passw']
        # Check if account exists in DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s',(email, password))
        # Fetch account
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            return 'Logged in'            
    else:
        return render_template("backTest.html")

    return render_template('index.html')


@app.route('/api', methods=['POST', 'GET'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'passw' in request.form and 'email' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['passw']


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == '__main__':
    app.run(debug=True)

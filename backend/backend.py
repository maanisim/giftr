# Really basic program for now
from flask import Flask, redirect, url_for, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, re, hashlib
app = Flask(__name__)

# DB Connection details
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'web'
# app.config['MYSQL_PASSWORD'] = 'AN(G3hg93hgn2ffim'
# app.config['MYSQL_DB'] = 'dummy'

# Initialise DB
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("backTest.html")


@app.route('/api', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'passw' in request.form:
        email = request.form['email']
        password = hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()
        # Check if account exists in DB
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s',(email, password))
        # # Fetch account
        # account = cursor.fetchone()
        return redirect(url_for("user", usr=email))

    #     if account:
    #         session['loggedin'] = True
    #         session['id'] = account['id']
    #         session['email'] = account['email']
    #         return 'Logged in'            
    # else:
    #     return render_template("backTest.html")

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

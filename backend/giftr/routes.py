from giftr import app, mysql
from flask import Flask, redirect, url_for, render_template, request, session, make_response
from flask_mysqldb import MySQLdb
import ssl, hashlib, re, datetime, smtplib, sys
from math import floor as floor

global COOKIE_TIME_OUT
COOKIE_TIME_OUT = 60*60*24*7  # 7 days

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

from sklearn.neighbors import NearestNeighbors
import numpy as np

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
        password = hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()
        #password = request.form['passw']

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
            #if(session['gender'] == "male" or session['gender'] == "female" or session['gender'] == "unisex"):
            session['gender'] = account['gender']
            session['age'] = account['age']
            alreadyRecc = onLoad()
            session["AlreadyRecc"] = alreadyRecc
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
            return render_template('login.html', msg=msg)
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
        username = request.form['username']
        name = request.form['name']
        password = hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()
        confirmPassword = hashlib.sha256(request.form['repeat_passw'].encode('utf-8')).hexdigest()
        email = request.form['email']
        bdaymonth = request.form['bdaymonth']
        bdaymonth = bdaymonth.split('-')
        age = floor(int((((datetime.datetime.now().year - int(bdaymonth[0])) * 12) + int(bdaymonth[1]))/12))
        gender = str(request.form.get('gender'))
        token = "TEST"
        photo = "default.png"

        count = 0
        if not re.match(r'[A-Za-z]+', name):
            msg = 'Name must contain only characters!'
            count += 1
        if not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            count += 1
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            msg = 'Invalid email address!'
            count += 1
        if password != confirmPassword:
            msg = 'Passwords do not match.'
            count += 1
        if len(request.form['passw']) < 7:
            msg = 'Password must be at least 7 characters long.'
            count += 1
        if len(email) < 5:
            msg = 'Email must be at least 5 characters long.'
            count+=1
        if not username or not password or not confirmPassword or not email or not bdaymonth or not gender:
            msg = 'Please fill out the form!'
            count += 1

        account = False
        if count == 0:
            # Check if account exists
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', [email])
            # Fetch account
            account = cursor.fetchone()

        if account:
            msg = 'Email already exists!'
            count += 1

        # All checks passed - insert to database
        if count == 0:
            cursor.execute('INSERT INTO users (username, password, token, email, name, age, gender, photo)'
                           'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (username, password, token, email, name, age, gender, photo))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('welcome'))

        if count > 1:
            msg='Please correctly fill out the form'
            
        return render_template('register.html', msg=msg)
    elif not 'loggedin' in session:
        return render_template('register.html')
    elif 'loggedin' in session:
        return render_template('index.html')
        


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('email', None)
        session.pop("AlreadyRecc", None)
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
    return render_template('search_for_gift.html')


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
        emailPassword = "Tataract52"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, emailPassword)
            server.sendmail(sender_email, receiver_email, message)
    return render_template('emailSent.html')


@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    print("welcome")
    if 'loggedin' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return "<h1>test</h1>"


@app.route('/new_settings',methods=['POST'])
def new_settings():
    if('loggedin' in session and request.method == 'POST'):
        #if(request.form['email'] == request.form['confirmEmail']):
        email = request.form['email']
            #if(len(email) > 4):
                #if(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)):
        print("email changed! to"+email)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE users set email=\"%s\" WHERE user_id",(id))

                    #print that something happened? to user
                    
        if(request.form['passw'] == request.form['cofirmPassw']):
            passw = request.form['passw']
            if(len(passw) > 7):
                if(re.match("^[A-Za-z0-9_-]*$", passw)):
                    print("pass changed! to"+passw)
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("UPDATE users set password=\"%s\" WHERE user_id",(passw))
                    #print that something happened? to user
        mysql.connection.commit()
    return render_template('settings.html')

        # ADD TO WISHLIST
        # if 'loggedin' in session:
        #     uid = session['id']
        #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #     cursor.execute('INSERT INTO wishlist_list WHERE user_id = %s VALUES %s', (uid, pid))
        #     data = cursor.fetchone()
        # else:
        #     return render_template(url_for(pid), msg="Please log in before adding to a wishlist!")

#+------------+-----------------------------+-------+---------+----------+-------+------------------------------------------------------------------------------------------+--------+--------------+
#| product_id | name                        | photo | age_low | age_high | price | link                                                                                     | gender | category     |
#+------------+-----------------------------+-------+---------+----------+-------+------------------------------------------------------------------------------------------+--------+--------------+
#|          1 | FITFORT Alarm Clock Wake Up | 1.jpg |      20 |       99 | $     | https://www.amazon.co.uk/FITFORT-Alarm-Clock-Wake-Light-Sunrise/dp/B07CQVM7WY/ref=sr_1_6 | unisex | Alarm Clocks |
#+------------+-----------------------------+-------+---------+----------+-------+------------------------------------------------------------------------------------------+--------+--------------+

@app.route('/p/<int:pid>', methods=['POST', 'GET'])
def product(pid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM products WHERE product_id = %s', [pid])
    item = cursor.fetchone()
    item_name = item['name']
    photo_name = item['photo']
    item_link = item['link']

    if request.method == 'POST':
        msg = ""
        if 'loggedin' in session:
            uid = session['id']
            if request.form['like']:
                print(str(uid)+":u LIKE - p:"+str(pid), file=sys.stderr)
                cursor.execute('INSERT INTO product_liked (product_id, user_id) VALUES (%s, %s)', (pid, uid))
            elif request.form['wish']:
                print(str(uid)+":u WISH - p:"+str(pid), file=sys.stderr)
                cursor.execute('INSERT INTO wishlist_list (product_id, user_id) VALUES (%s, %s)', (pid, uid))
        else:
            msg="Please log in before adding to a wishlist!"
        mysql.connection.commit()

    return render_template('item_backend.html',
    item_name=item_name,
    photo_name=photo_name,
    item_link=item_link )
    # --------------------------- STATIC ROUTES --------------------------------------------------

@app.route('/settings')
def settings():
    if 'loggedin' in session:
        return render_template('settings.html')
    return render_template('404.html')


@app.route('/questionnaire')
def questionnaire():
    if 'loggedin' in session:
        return render_template('rQuestionnaire.html')
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

@app.route('/friends')
def friends():
    if 'loggedin' in session:
        return render_template('my_friends.html')
    return render_template('404.html')

@app.route('/questionaire')
def questionaire():
    if 'loggedin' in session:
        return render_template('rQuestionnaire.html')
    return render_template('404.html')

@app.route('/item')
def item():
    return render_template('itemPage.html')


@app.route('/wishlist')
def wishlist():
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM wishlist WHERE user_id = %s', [user_id])
        # Fetch wishlist
        wishlist_data = cursor.fetchone()

        return render_template('wishlist.html')
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy_policy.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/suggestion')
def suggestion():
    if 'loggedin' in session:
        update()
        alreadyRecc = session["AlreadyRecc"]
        recommendation = Recommendation(session["id"], alreadyRecc)
        image = "img/p/" + recommendation["photo"]
        alreadyRecc = updateAlreadyRecc(recommendation, alreadyRecc)
        session["AlreadyRecc"] = alreadyRecc
        session["recommendation"] = recommendation
        return render_template('itemSuggestion.html', recommendation=recommendation, image = image)
    return render_template('index.html')

@app.route('/suggestion1')
def suggestion1():
    alreadyRecc = session["AlreadyRecc"]
    recommendation = session["recommendation"]
    updateValues("yes", recommendation, session["id"])
    recommendation = Recommendation(session["id"], alreadyRecc)
    image = "img/p/" + recommendation["photo"]
    session["recommendation"] = recommendation
    return render_template('itemSuggestion.html', recommendation=recommendation, image = image)

@app.route('/suggestion2')
def suggestion2():
    alreadyRecc = session["AlreadyRecc"]
    recommendation = session["recommendation"]
    updateValues("no", recommendation, session["id"])
    recommendation = Recommendation(session["id"], alreadyRecc)
    image = "img/p/" + recommendation["photo"]
    session["recommendation"] = recommendation
    return alreadyRecc
    #return render_template('itemSuggestion.html', recommendation=recommendation, image = image)
###################################################################
#Functions for Suggestion
###################################################################
def update():

    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    crsr.execute("SELECT product_id FROM products")
    existingProducts = crsr.fetchall()
    crsr.execute("SELECT product_id FROM productRecValues")
    presentIDs = crsr.fetchall()
    for product in existingProducts:
        if (product not in presentIDs):
            crsr.execute("SELECT * FROM products WHERE product_id = %d", product)
            counter = crsr.fetchall()             
            productID = counter["product_id"]
            age_low = round(counter["age_low"]*1.5)
            age_high = round(counter["age_high"]*1.5)
            if (counter["price"] == "$"):
                price = 100
            elif (counter["price"] == "$$"):
                price = 300
            elif (counter["price"] == "$$$"):
                price = 500
            else:
                price = 0
            if (counter["gender"] == "male"):
                gender1 = 500
                gender2 = 0
            elif (counter["gender"] == "female"):
                gender1 = 0
                gender2 = 500
            else:
                gender1 = 250
                gender2 = 250
            toiletries = 0
            clothes = 0
            homeware = 0
            entertainment = 0
            consumable = 0
            sport = 0
            other = 0
            if ((counter["category"] == "Bath Bombs") or
                (counter["category"] == "Perfumes") or
                (counter["category"] == "Skincare")):
                toiletries = 500

            elif((counter["category"] == "Belts") or
                 (counter["category"] == "Cufflinks") or
                 (counter["category"] == "Hats") or
                 (counter["category"] == "Jewllery") or
                 (counter["category"] == "Keyrings") or
                 (counter["category"] == "Scarfs") or
                 (counter["category"] == "Shoes") or
                 (counter["category"] == "Socks") or
                 (counter["category"] == "T-Shirts") or
                 (counter["category"] == "Wallets") or
                 (counter["category"] == "Watches")):
                clothes = 500
                
            elif((counter["category"] == "Alarm Clocks") or
                 (counter["category"] == "Blankets") or
                 (counter["category"] == "Chairs") or
                 (counter["category"] == "Cushionss") or
                 (counter["category"] == "Flowers") or
                 (counter["category"] == "Magnets") or
                 (counter["category"] == "Mugs") or
                 (counter["category"] == "Paintings") or
                 (counter["category"] == "Photo Frames") or
                 (counter["category"] == "World Maps")):
                homeware = 500
                
            elif((counter["category"] == "Board Games") or
                 (counter["category"] == "Cards") or
                 (counter["category"] == "Disney") or
                 (counter["category"] == "Headphones") or
                 (counter["category"] == "Teddy Bears") or
                 (counter["category"] == "Video Games") or
                 (counter["category"] == "Vinyl")):
                entertainment = 500

            elif((counter["category"] == "Biscuits") or
                 (counter["category"] == "Wine")):
                consumable = 500

            elif((counter["category"] == "Liverpool") or
                 (counter["category"] == "Manchester United")):
                sport = 500
                
            else:
                other = 500
                
            crsr.execute("""INSERT INTO productRecValues VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(productID, age_low, age_high, price, gender1, gender2, toiletries, clothes, homeware, entertainment, consumable, sport, other))
            
    crsr.execute("SELECT user_id FROM users")
    existingUsers = crsr.fetchall()
    crsr.execute("SELECT user_id FROM profileRecValues")
    presentIDs = crsr.fetchall()
    for user in existingUsers:
        if (user not in presentIDs):
            crsr.execute("SELECT * FROM users WHERE user_id = %d", user)
            counter = crsr.fetchall()
            userID = counter["user_id"]
            age = round(counter["age"]*1.5)
            if (counter["gender"] == "male"):
                gender1 = 500
                gender2 = 100
            elif (counter["gender"] == "female"):
                gender1 = 100
                gender2 = 500
            else:
                gender1 = 250
                gender2 = 250
               
            crsr.execute("""INSERT INTO profileRecValues VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (userID, age, age, 200, gender1, gender2, 250, 250, 250, 250, 250, 250, 250))

    mysql.connection.commit()
    
def onLoad():
    alreadyRecc = []
    return alreadyRecc

def Recommendation(currentUser, alreadyRecc):
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM productRecValues""")
    dataValuesDic = crsr.fetchall()
    userID = currentUser
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM
                profileRecValues WHERE user_id = '%d'""" % userID)
    userDataDic = crsr.fetchone()
    dataValues = []
    for counter in dataValuesDic:
        a = list(counter.values())
        a = np.array(a)
        dataValues.append(a)
    userData = np.array(list(userDataDic.values()))
    userData = [userData]
    neigh = NearestNeighbors(n_neighbors=1)
    neigh.fit(dataValues)
    reccID = neigh.kneighbors(userData, return_distance = False)
    reccID = reccID[0]
    recommendationsReq = 2
    while (reccID in alreadyRecc):
        neigh = NearestNeighbors(n_neighbors=recommendationsReq)
        neigh.fit(dataValues)
        reccID = neigh.kneighbors(userData, return_distance = False)
        foundRecc = False
        for counter in reccID:
            n = counter + 1
            if (n not in alreadyRecc):
                reccID = n
                foundRecc = True
        if (foundRecc == False):
            reccID = reccID["error"]
        recommendationsReq += 1
    crsr.execute("""SELECT * FROM products WHERE product_id = '%d'""" % reccID)
    recommendedProduct = crsr.fetchone()
    return recommendedProduct

def updateAlreadyRecc(recommendedProduct, alreadyRecc):
    if (len(alreadyRecc) > 50):
        del alreadyRecc[0]
    alreadyRecc.append(recommendedProduct)
    return alreadyRecc

def updateValues(result, recommendedProduct, currentUser):
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM
                profileRecValues WHERE user_id = '%d'""" % currentUser)
    userData = crsr.fetchone()
    userData = list(userData.values())
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM
                productRecValues WHERE product_id = '%d'""" % recommendedProduct["product_id"])
    productData = crsr.fetchone()
    productData = list(productData.values())
    if (result == "yes"):
        newUserValues = []
        newProductValues = []
        for counter in range(len(userData)):
            newValue = (userData[counter] - productData[counter])//2
            newUserValues.append(userData[counter] - newValue)
            newProductValues.append(productData[counter] + newValue)
            if (newUserValues[counter] > 900):
                newUserValue = 900
            if (newProductValues[counter] > 900):
                newProductValue = 900
            if (newUserValues[counter] < 0):
                newUserValue = 0
            if (newProductValues[counter] < 0):
                newProductValue = 0
    else:
        newUserValues = []
        newProductValues = []
        for counter in range(len(userData)):
            newValue = (userData[counter] - productData[counter])//2
            newUserValues.append(userData[counter] + newValue)
            newProductValues.append(productData[counter] - newValue)
            if (newUserValues[counter] > 900):
                newUserValues[counter] = 900
            if (newProductValues[counter] > 900):
                newProductValues[counter] = 900
            if (newUserValues[counter] < 0):
                newUserValues[counter] = 0
            if (newProductValues[counter] < 0):
                newProductValues[counter] = 0
    crsr.execute("""UPDATE profileRecValues
                SET age_low = '%s', age_high = '%s', price = '%s', gender1 = '%s', gender2 = '%s', toiletries = '%s',
                clothes = '%s', homeware = '%s', entertainment = '%s', consumable = '%s', sport = '%s', other = '%s'
                WHERE user_id = '%s'""", (newUserValues[0], newUserValues[1], newUserValues[2],
                newUserValues[3], newUserValues[4], newUserValues[5], newUserValues[6],
                newUserValues[7], newUserValues[8], newUserValues[9], newUserValues[10],
                newUserValues[11], currentUser))
    crsr.execute("""UPDATE productRecValues
                SET age_low = '%s', age_high = '%s', price = '%s', gender1 = '%s', gender2 = '%s', toiletries = '%s',
                clothes = '%s', homeware = '%s', entertainment = '%s', consumable = '%s', sport = '%s', other = '%s'
                WHERE product_id = '%s'""", (newProductValues[0], newProductValues[1], newProductValues[2],
                newProductValues[3], newProductValues[4], newProductValues[5], newProductValues[6],
                newProductValues[7], newProductValues[8], newProductValues[9], newProductValues[10],
                newProductValues[11], recommendedProduct["product_id"]))
    mysql.connection.commit()

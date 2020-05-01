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
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #take out all products with the highest amount of likes
    cursor.execute(f"SELECT products.product_id,products.name,products.photo 
    FROM products,(SELECT `product_id`,COUNT(`product_id`) AS `value_occurrence` 
    FROM `product_liked` GROUP BY `product_id` ORDER BY `value_occurrence` DESC LIMIT 12) 
    AS top12 WHERE top12.product_id = products.product_id")
    top12items = cursor.fetchall()
    mysql.connection.commit()
    #if logged in keep the username variable in nav bar
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'],top12items=top12items)
    return render_template('index.html',top12items=top12items)



#Authenticate the user with email and password
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

#Register the user with common registration info
@app.route('/register', methods=['POST', 'GET'])
def register():
    # if not yet logged in
    if not 'loggedin' in session and request.method == 'POST' and 'name' in request.form and 'passw' in request.form and 'email' in request.form:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist

        #  All the details user registers
        username = request.form['username']
        name = request.form['name']
        password = hashlib.sha256(request.form['passw'].encode('utf-8')).hexdigest()
        confirmPassword = hashlib.sha256(request.form['repeat_passw'].encode('utf-8')).hexdigest()
        email = request.form['email']
        bdaymonth = request.form['bdaymonth']
        bdaymonth = bdaymonth.split('-')
        # as suggested by our reviewer for privacy reasons we take away the day from the dob in order to 
        age = floor(int((((datetime.datetime.now().year - int(bdaymonth[0])) * 12) + int(bdaymonth[1]))/12))
        gender = str(request.form.get('gender'))
        #In case we need to input users cookie into the database (we didn't had to yet) we create a token variable which can hold it
        token = "TEST"
        #users_picture
        photo = "default.png"

        #count errors
        count = 0
        # checking cases by counting errors
        if not re.match(r'[A-Za-z]+', name):
            msg = 'Name must contain only [A-Za-z] characters!'
            count += 1
        if not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only [A-Za-z0-9] characters!'
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
            return redirect(url_for('index'))

        if count > 1:
            msg='Please correctly fill out the form'
            
        return render_template('register.html', msg=msg)
    elif not 'loggedin' in session:
        return render_template('register.html')
    elif 'loggedin' in session:
        return render_template('index.html')
        

# logs user out by clearing cookies and redirecting to index page
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'loggedin' in session:
        # log out user
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('email', None)
        session.pop("AlreadyRecc", None)
        return redirect('/')
    return redirect('/')

# redirects user to their profile page (cookies needed)
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('my_profile.html', username=session['username'])
    return redirect('/')

#searches for the products on the website by dynamically generating content
@app.route('/search', methods=['POST', 'GET'])
def search():
    # If request sent
    if(request.method == 'POST' and 'search' in request.form):
        search = request.form['search']
        # If request not sql injection
        if(re.match("^[A-Za-z0-9_-]*$", search) is not None):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM products WHERE products.name LIKE '%{search}%' LIMIT 25")
            items = cursor.fetchall()
            return render_template('search_for_gift.html', items=items)

    # USING FILTERS
    if request.method == 'POST' and 'searchbox' in request.form:
        # variables for category search types
        search = request.form['searchbox']
        sort = request.form.get('sort')
        price = request.form.get('price')
        age = request.form.get('age')


        # Let user choose price in their search category
        andPrice = " AND products.price = "
        if int(price) == 0:
            andPrice = ""
        elif int(price) == 1:
            andPrice += "'$'"
        elif int(price) == 2:
            andPrice += "'$$'"
        elif int(price) == 3:
            andPrice += "'$$$'"
        elif int(price) == 4:
            andPrice += "'$$$$'"

        # sql statment for age IE age = a than if (x>=a && y<=a) show product
        andAge = ""
        if age:
            andAge = f" AND {age} BETWEEN products.age_low AND products.age_high"

        male = 'male' if request.form.get('male') else None
        female = 'female' if request.form.get('female') else None
        unisex = 'unisex' if request.form.get('unisex') else None

        genders = [male, female, unisex]
        #let user choose gender male female or unisex in their search category
        if(re.match("^[A-Za-z0-9_-]*$", search) is not None):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # different statements for different amounts of variables
            if len(genders) == 3 or not genders:
                cursor.execute(f"SELECT * FROM products WHERE products.name LIKE '%{search}%'{andPrice}{andAge} ORDER BY products.name {sort} LIMIT 25")
                items = cursor.fetchall()
                mysql.connection.commit()
                return render_template('search_for_gift.html', items=items)
            elif len(genders) == 2:
                cursor.execute(f"SELECT * FROM products WHERE gender = {genders[0]} AND gender = {genders[1]} AND products.name LIKE '%{search}%'{andPrice}{andAge} ORDER BY products.name {sort} LIMIT 25")
                items = cursor.fetchall()
                return render_template('search_for_gift.html', items=items)
                
            elif len(genders) == 1:
                cursor.execute(f"SELECT * FROM products WHERE gender = {genders[0]} AND products.name LIKE '%{search}%'{andPrice}{andAge} ORDER BY products.name {sort} LIMIT 25")
                items = cursor.fetchall()
                
                return render_template('search_for_gift.html', items=items)

    return render_template('search_for_gift.html')

#old school search bar, had to be disable due to sql injection found by our penetration testing team
@app.route('/search2', methods=['POST', 'GET'])
def search2():
    # SEARCH WITH NO PARAMS
    if(request.method == 'POST' and 'search' in request.form):
        search = request.form['search']
        if(re.match("^[A-Za-z0-9_-]*$", search) is not None):
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute(f"SELECT * FROM products WHERE products.name LIKE '%{search}%' LIMIT 25")
                    items = cursor.fetchall()
                    return render_template('search_for_gift2.html', items=items)

    # USING FILTERS
    if request.method == 'POST' and 'searchbox' in request.form:
        # OPTIONS

        search = request.form['searchbox']
        sort = request.form.get('sort')

        male = 'male' if request.form.get('male') else None
        female = 'female' if request.form.get('female') else None
        unisex = 'unisex' if request.form.get('unisex') else None

        genders = [male, female, unisex]

        if(re.match("^[A-Za-z0-9_-]*$", search) is not None):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if len(genders) == 3 or not genders:
                cursor.execute(f"SELECT * FROM products WHERE products.name LIKE '%{search}%' ORDER BY products.name {sort} LIMIT 25")
                items = cursor.fetchall()
                print(items, file=sys.stderr)
                mysql.connection.commit()
                return render_template('index.html', items=items)

            elif len(genders) == 2:
                cursor.execute(f"SELECT * FROM products WHERE gender = {genders[0]} AND gender = {genders[1]} AND products.name LIKE '%{search}%' ORDER BY products.name {sort} LIMIT 25", (genders[0], genders[1], search))
                items = cursor.fetchall()
                return render_template('index.html', items=items)
                
            elif len(genders) == 1:
                cursor.execute(f"SELECT * FROM products WHERE gender = {genders[0]} AND products.name LIKE '%{search}%' ORDER BY products.name {sort} LIMIT 25", (genders[0], search))
                items = cursor.fetchall()
                
                return render_template('index.html', items=items)

    return render_template('index.html')


@app.route('/emailSent', methods=['POST', 'GET'])
def emailsent():
    '''
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
        emailPassword = "passwordhere"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, emailPassword)
            server.sendmail(sender_email, receiver_email, message)
            '''
            #return render_template('emailSent.html')
    return render_template('index.html')

#updates the old settings to new, for now we do not allow to change password however it's ready to be implement at any time
@app.route('/new_settings',methods=['POST'])
def new_settings():
    if('loggedin' in session and request.method == 'POST'):
        uid = session['id']
        if(request.form['email'] == request.form['confirmEmail']):
            email = request.form['email']
            if(len(email) > 4):
                if(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)):
                    print("email changed! to"+email+" user_id= "+str(uid))
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    #cursor.execute("UPDATE users set email=%s WHERE user_id=%s",(email,uid))
                    cursor.execute('SELECT * FROM users WHERE email = %s', [email])
                    check = cursor.fetchone()
                    if not check:
                        cursor.execute(f"UPDATE users set email= '{email}' WHERE user_id={uid}")
                        session.pop('email', None)
                        session['email'] = email
                    #request.form['email'] = email
                    #print that something happened? to user
                    
            #if(request.form['passw'] == request.form['cofirmPassw']):
             #   passw = request.form['passw']
             #   if(len(passw) > 7):
             #       if(re.match("^[A-Za-z0-9_-]*$", passw)):
             #           print("pass changed! to"+passw)
             #           cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             #           cursor.execute("UPDATE users set password=\"%s\" WHERE user_id=%s",(passw,uid))
             #           #print that something happened? to user
        mysql.connection.commit()
        return render_template('settings.html')
    else:
        return render_template('index.html')
        # ADD TO WISHLIST
        # if 'loggedin' in session:
        #     uid = session['id']
        #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #     cursor.execute('INSERT INTO wishlist_list WHERE user_id = %s VALUES %s', (uid, pid))
        #     data = cursor.fetchone()
        # else:
        #     return render_template(url_for(pid), msg="Please log in before adding to a wishlist!")

# Exmaple page giftr.cf/p/1800 or https://giftr.cf/p/23
# We generate the product pages based on pid from the database.
@app.route('/p/<int:pid>', methods=['POST', 'GET'])
def product(pid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM products WHERE product_id = %s', [pid])

    # setting variables
    item = cursor.fetchone()
    item_name = item['name']
    photo_name = item['photo']
    item_link = item['link']
    item_gender = item['gender']
    item_category = item['category']
    age_high = item['age_high']
    age_low = item['age_low']
    item_price = item['price']

    # if post then check form value, if its like add to the liked products db, if its wishlist, add to wishlist
    if request.method == 'POST':
        msg = ""
        if 'loggedin' in session:
            uid = session['id']
            if request.form.get('like'):
                # CHECKING DUPLICATE
                cursor.execute('SELECT * FROM product_liked WHERE product_id = %s AND user_id = %s', (pid, uid))
                check = cursor.fetchone()
                if not check:
                    cursor.execute('INSERT INTO product_liked (product_id, user_id) VALUES (%s, %s)', (pid, uid))
            elif request.form.get('wish'):
                # CHECKING DUPLICATE
                cursor.execute('SELECT * FROM wishlist_list WHERE product_id = %s AND user_id = %s', (pid, uid))
                check = cursor.fetchone()
                if not check:
                    cursor.execute('INSERT INTO wishlist_list (product_id, user_id) VALUES (%s, %s)', (pid, uid))
        else:
            msg="Please log in before adding to a wishlist!"
        mysql.connection.commit()
        update()

    # render all variables on item page
    return render_template('itemPage.html',
    item_name=item_name,
    photo_name=photo_name,
    item_link=item_link,
    item_gender=item_gender,
    item_category=item_category,
    age_high=age_high,
    age_low=age_low,
    item_price=item_price
    )

# render a user's page based on their user_id in the database. We were debating whether to user user_id or username and decided for now to use user_id.
@app.route('/u/<int:uid>', methods=['POST', 'GET'])
def user(uid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE user_id = %s', [uid])
    user = cursor.fetchone()
    username = user['username']

    return render_template('anotherProfile.html',
    username=username,
    )

# display wishlist/gift bank items based on what user had choosen
@app.route('/wishlist')
def wishlist():
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT products.product_id, products.name, products.photo FROM wishlist_list INNER JOIN products ON wishlist_list.product_id=products.product_id WHERE user_id=%s', [user_id])
        # Fetch wishlist
        
        wishlist_data = cursor.fetchall()
        print(wishlist_data)
        mysql.connection.commit()
        return render_template('wishlist.html',wishlist_data=wishlist_data)
    return redirect(url_for('index'))

# --------------------------- STATIC ROUTES --------------------------------------------------

#/settings page showcases users settings which are changeable
@app.route('/settings')
def settings():
    if 'loggedin' in session:
        return render_template('settings.html')
    return render_template('index.html')

#/questionnaire page showcases questionnaire which is used in order to make AI more targeted to the user
@app.route('/questionnaire')
def questionnaire():
    if 'loggedin' in session:
        return render_template('rQuestionnaire.html')
    return render_template('404.html')

#/forgot page showcases forgot password page which has not been yet implement due to not being able to find a free email service.
@app.route('/forgot')
def forgot():
    if 'loggedin' in session:
        return render_template('index.html')
    return render_template('forgotPsw.html')

#test page used to test whether /friend page worked (to be delted)
@app.route('/friend')
def friend():
    if 'loggedin' in session:
        return render_template('anotherProfile.html')
    return render_template('404.html')

#/friends showcases friends of the currently logged in user (not yet implemented)
@app.route('/friends')
def friends():
    if 'loggedin' in session:
        return render_template('my_friends.html')
    return render_template('404.html')

#test page used to test whether /item page worked (to be delted)
@app.route('/item')
def item():
    return render_template('itemPage.html')


#/about page used to showcase the about info about the website
@app.route('/about')
def about():
    return render_template('about.html')

#/privacy page used to showcase the privacy info about the website
@app.route('/privacy')
def privacy():
    return render_template('privacy_policy.html')

#/contact page used to showcase the contact info about the website
@app.route('/contact')
def contact():
    return render_template('contact.html')


# --------------------------- Aritficial Inteligence --------------------------------------------------

#############################################################
#Suggestions
#############################################################

#initial suggestion
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
        pid = recommendation["product_id"]
        return render_template('itemSuggestion.html', recommendation=recommendation, image = image, pid=pid)
    return redirect(url_for('index'))

#handle suggestion if liked
@app.route('/suggestion1')
def suggestion1():
    alreadyRecc = session["AlreadyRecc"]
    recommendation = session["recommendation"]
    updateValues("yes", recommendation, session["id"])
    liked(recommendation)
    recommendation = Recommendation(session["id"], alreadyRecc)
    image = "img/p/" + recommendation["photo"]
    session["recommendation"] = recommendation
    alreadyRecc = updateAlreadyRecc(recommendation, alreadyRecc)
    pid = recommendation["product_id"]
    return render_template('itemSuggestion.html', recommendation=recommendation, image = image, pid=pid)

#Handle suggestion if disliked
@app.route('/suggestion2')
def suggestion2():
    alreadyRecc = session["AlreadyRecc"]
    recommendation = session["recommendation"]
    updateValues("no", recommendation, session["id"])
    recommendation = Recommendation(session["id"], alreadyRecc)
    image = "img/p/" + recommendation["photo"]
    session["recommendation"] = recommendation
    alreadyRecc = updateAlreadyRecc(recommendation, alreadyRecc)
    pid = recommendation["product_id"]
    return render_template('itemSuggestion.html', recommendation=recommendation, image = image, pid=pid)
###################################################################
#Functions for Suggestion
###################################################################

#Handles any update to product database or user database
def update():
    #Import values
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    crsr.execute("SELECT product_id FROM products")
    existingProducts = crsr.fetchall()
    crsr.execute("SELECT product_id FROM productRecValues")
    presentIDs = crsr.fetchall()
    #Assigns numerical values for all new products
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
    
    #Assigns numerical values for new users
    crsr.execute("SELECT user_id FROM users")
    existingUsers = crsr.fetchall()
    crsr.execute("SELECT user_id FROM profileRecValues")
    presentIDs = crsr.fetchall()
    for user in existingUsers:
        if (user not in presentIDs):
            a = user["user_id"]
            crsr.execute("SELECT * FROM users WHERE user_id = '%s'" % a)
            counter = crsr.fetchone()
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

#generates initial list that stores items that have already been recommened
def onLoad():
    alreadyRecc = []
    return alreadyRecc

#Returns recommended product
def Recommendation(currentUser, alreadyRecc):
    #Pull values from database
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM productRecValues""")
    dataValuesDic = crsr.fetchall()
    userID = currentUser
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM
                profileRecValues WHERE user_id = '%d'""" % userID)
    userDataDic = crsr.fetchone()
    #Put values in correct data format
    dataValues = []
    for counter in dataValuesDic:
        a = list(counter.values())
        a = np.array(a)
        dataValues.append(a)
    userData = np.array(list(userDataDic.values()))
    userData = [userData]
    #Set model
    neigh = NearestNeighbors(n_neighbors=1)
    neigh.fit(dataValues)
    #Generate recommendation
    reccID = neigh.kneighbors(userData, return_distance = False)
    reccID = reccID[0][0]
    recommendationsReq = 2
    #Ensures recommendation has not already been given
    while (reccID in alreadyRecc):
        neigh = NearestNeighbors(n_neighbors=recommendationsReq)
        neigh.fit(dataValues)
        reccID = neigh.kneighbors(userData, return_distance = False)
        foundRecc = False
        for counter in reccID[0]:
            n = counter
            if (n not in alreadyRecc):
                reccID = n
                foundRecc = True
        if (foundRecc == False):
            reccID = reccID[0][0]
        recommendationsReq += 1
    #produces recommendation
    crsr.execute("""SELECT * FROM products WHERE product_id = '%d'""" % reccID)
    recommendedProduct = crsr.fetchone()
    return recommendedProduct

#Update array of gifts already shown to user
def updateAlreadyRecc(recommendedProduct, alreadyRecc):
    if (len(alreadyRecc) > 50):
        del alreadyRecc[0]
    alreadyRecc.append(recommendedProduct["product_id"])
    return alreadyRecc

#Refine product and user values, ensures "learning"
def updateValues(result, recommendedProduct, currentUser):
    #Pull values from database
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
    #Modifies values if product is liked
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
    #Modifies values if product is disliked
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
    #Update database with new values
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

#Adds liked product to likes and wishlist
def liked(recommendation):
    uid = session['id']
    pid = recommendation["product_id"]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM product_liked WHERE product_id = %s AND user_id = %s', (pid, uid))
    check = cursor.fetchone()
    if not check:
        cursor.execute('INSERT INTO product_liked (product_id, user_id) VALUES (%s, %s)', (pid, uid))
                # CHECKING DUPLICATE
    cursor.execute('SELECT * FROM wishlist_list WHERE product_id = %s AND user_id = %s', (pid, uid))
    check = cursor.fetchone()
    if not check:
        cursor.execute('INSERT INTO wishlist_list (product_id, user_id) VALUES (%s, %s)', (pid, uid))
    mysql.connection.commit()

########################################################################
#IMPORTS: IMPORTANT
########################################################################

from sklearn.neighbors import NearestNeighbors
import numpy as np
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="myusername",
  passwd="mypassword"
  database = "database"
)
#####################################################################################
#ALL INFO WITHIN CONNECTION SHOULD BE REPLACED WITH RELEVANT HOST, USERNAME, PASSWORD AND
#DATABASE NAME DETAILS
#####################################################################################

#######################################################################################
#GENERATES DATABASE FOR TESTING PURPOSES, SHOULD NOT BE RUN ONCE CONNECTED TO DATABASE
#######################################################################################
def createDB():
    connection = mysql.connector.connect(
          host="localhost",
          user="myusername",
          passwd="mypassword"
          database = "database"
    )
    crsr = connection.cursor()
    fd = open('products.sql','r')
    createProducts = fd.read()
    fd.close()
    fd = open('insert.sql','r')
    insert = fd.read()
    fd.close()
    fd = open('users.sql','r')
    createUsers = fd.read()
    fd.close
    crsr.execute(createProducts)
    crsr.execute(insert)
    crsr.execute(createUsers)
    exampleUser = """INSERT INTO users(username, password, token, email, name, age, gender)
                    VALUES("RufusW", "password", "sample", "sample", "Rufus", 19, "male")"""
    crsr.execute(exampleUser)
    connection.commit()
    connection.close()


########################################################################################
#SHOULD BE RUN ONCE TO GENERATE INFRASTRUCTURE FOR RECOMMENDATIONS
########################################################################################
def initialise():
    connection = mysql.connector.connect(
          host="localhost",
          user="myusername",
          passwd="mypassword"
          database = "database"
    )
    crsr = connection.cursor()
    createValues = """CREATE TABLE productRecValues (
                'product_id' INT(10) NOT NULL,
                'age_low' INT(3) NOT NULL,
                'age_high' INT(3) NOT NULL, 
                'price' INT(3) NOT NULL,
                'gender1' INT(3) NOT NULL,
                'gender2' INT(3) NOT NULL,
                'toiletries' INT(3) NOT NULL,
                'clothes' INT(3) NOT NULL,
                'homeware' INT(3) NOT NULL,
                'entertainment' INT(3) NOT NULL,
                'consumable' INT(3) NOT NULL,
                'sport' INT(3) NOT NULL,
                'other' INT(3) NOT NULL,
                PRIMARY KEY(product_id),
                FOREIGN KEY(product_id) REFERENCES products(product_id)
                )"""

    createProfiles = """CREATE TABLE profileRecValues (
                'user_id' INT(10) NOT NULL,
                'age_low' INT(3) NOT NULL,
                'age_high' INT(3) NOT NULL,
                'price' INT(3) NOT NULL,
                'gender1' INT(3) NOT NULL,
                'gender2' INT(3) NOT NULL,
                'toiletries' INT(3) NOT NULL,
                'clothes' INT(3) NOT NULL,
                'homeware' INT(3) NOT NULL,
                'entertainment' INT(3) NOT NULL,
                'consumable' INT(3) NOT NULL,
                'sport' INT(3) NOT NULL,
                'other' INT(3) NOT NULL,
                PRIMARY KEY(user_id),
                FOREIGN KEY(user_id) REFERENCES users(user_id)
                )"""

    crsr.execute(createValues)
    crsr.execute(createProfiles)
    connection.commit()
    connection.close()
    
##########################################################################################
#SHOULD BE RUN WHENEVER ITEMS ADDED TO DATABASE POPULATES DATABASE 
##########################################################################################
def update():
    connection = mysql.connector.connect(
          host="localhost",
          user="myusername",
          passwd="mypassword"
          database = "database"
    )
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM products")
    existingProducts = crsr.fetchall()
    crsr.execute("SELECT product_id FROM productRecValues")
    presentIDs = crsr.fetchall()
    for counter in existingProducts:
        if ((counter[0],) not in presentIDs):
            productID = counter[0]
            age_low = round(counter[3]*1.5)
            age_high = round(counter[4]*1.5)
            if (counter[5] == "$"):
                price = 100
            elif (counter[5] == "$$"):
                price = 300
            elif (counter[5] == "$$$"):
                price = 500
            else:
                price = 0
            if (counter[7] == "male"):
                gender1 = 500
                gender2 = 0
            elif (counter[7] == "female"):
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
            if ((counter[8] == "Bath Bombs") or
                (counter[8] == "Perfumes") or
                (counter[8] == "Skincare")):
                toiletries = 500

            elif((counter[8] == "Belts") or
                 (counter[8] == "Cufflinks") or
                 (counter[8] == "Hats") or
                 (counter[8] == "Jewllery") or
                 (counter[8] == "Keyrings") or
                 (counter[8] == "Scarfs") or
                 (counter[8] == "Shoes") or
                 (counter[8] == "Socks") or
                 (counter[8] == "T-Shirts") or
                 (counter[8] == "Wallets") or
                 (counter[8] == "Watches")):
                clothes = 500
                
            elif((counter[8] == "Alarm Clocks") or
                 (counter[8] == "Blankets") or
                 (counter[8] == "Chairs") or
                 (counter[8] == "Cushionss") or
                 (counter[8] == "Flowers") or
                 (counter[8] == "Magnets") or
                 (counter[8] == "Mugs") or
                 (counter[8] == "Paintings") or
                 (counter[8] == "Photo Frames") or
                 (counter[8] == "World Maps")):
                homeware = 500
                
            elif((counter[8] == "Board Games") or
                 (counter[8] == "Cards") or
                 (counter[8] == "Disney") or
                 (counter[8] == "Headphones") or
                 (counter[8] == "Teddy Bears") or
                 (counter[8] == "Video Games") or
                 (counter[8] == "Vinyl")):
                entertainment = 500

            elif((counter[8] == "Biscuits") or
                 (counter[8] == "Wine")):
                consumable = 500

            elif((counter[8] == "Liverpool") or
                 (counter[8] == "Manchester United")):
                sport = 500
                
            else:
                other = 500
            crsr.execute("""INSERT INTO productRecValues VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (productID, age_low, age_high,
                        price, gender1, gender2, toiletries, clothes, homeware,
                        entertainment, consumable, sport, other))

    crsr.execute("SELECT * FROM users")
    existingUsers = crsr.fetchall()
    crsr.execute("SELECT user_id FROM profileRecValues")
    presentIDs = crsr.fetchall()
    for counter in existingUsers:
        if ((counter[0],) not in presentIDs):
            userID = counter[0]
            age = round(counter[6]*1.5)
            if (counter[7] == "male"):
                gender1 = 500
                gender2 = 100
            elif (counter[7] == "female"):
                gender1 = 100
                gender2 = 500
            else:
                gender1 = 250
                gender2 = 250
            crsr.execute("""INSERT INTO profileRecValues VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                         (userID, age, age, 200, gender1, gender2, 250, 250, 250, 250, 250, 250, 250))
    connection.commit()
    connection.close()

#####################################################################################
#SHOULD BE RUN UPON LOADING RECOMMENDATIONS
#####################################################################################
def onLoad():
    alreadyRecc = []
    return alreadyRecc

#####################################################################################
#GENERATES RECOMMENDATIONS, RETURNS RECOMMENDATION AS ELEMENT IN PRODUCT TABLE
#####################################################################################
#NOTE: CurrentUser is user_id of the logged in user, must be accessed before running

def Recommendation(currentUserID, alreadyRecc):
    connection = mysql.connector.connect(
          host="localhost",
          user="myusername",
          passwd="mypassword"
          database = "database"
    )
    crsr = connection.cursor()
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM productRecValues""")
    dataValues = crsr.fetchall()
    userID = currentUser
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM
                profileRecValues WHERE user_id = '%d'""" % userID)
    userData = crsr.fetchall()
    neigh = NearestNeighbors(n_neighbors=1)
    neigh.fit(dataValues)
    reccID = neigh.kneighbors(userData, return_distance = False)
    reccID = reccID[0][0] + 1
    recommendationsReq = 2
    while (reccID in alreadyRecc):
        neigh = NearestNeighbors(n_neighbors=recommendationsReq)
        neigh.fit(dataValues)
        reccID = neigh.kneighbors(userData, return_distance = False)
        foundRecc = False
        for counter in reccID[0]:
            n = counter + 1
            if (n not in alreadyRecc):
                reccID = n
                foundRecc = True
        if (foundRecc == False):
            reccID = reccID[0][0]
        recommendationsReq += 1
    crsr.execute("""SELECT * FROM products WHERE product_id = '%d'""" % reccID)
    recommendedProduct = crsr.fetchall()
    connection.close()
    return recommendedProduct

###################################################################################
#SHOULD BE RUN AFTER RECOMMENDATION DISPLAYED
###################################################################################
def updateAlreadyRecc(recommendedProduct, alreadyRecc):
    if (len(alreadyRecc) > 50):
        del alreadyRecc[0]
    alreadyRecc.append(recommendedProduct[0][0])
    return alreadyRecc

###################################################################################
#IO USED FOR TESTING, NOT REQUIRED IN FINAL CODE
###################################################################################
def IO(recommendedProduct):
    print(recommendedProduct[0][1])
    result = input("Like? ")
    result = result.lower()
    return result

###################################################################################
#SHOULD BE RUN EVERY TIME AFTER YES/NO SELECTED ON PRODUCT
###################################################################################
#NOTE: result is whether the user has liked the product, in the form "yes" or "no"
def updateValues(result, recommendedProduct, currentUser):
    connection = mysql.connector.connect(
          host="localhost",
          user="myusername",
          passwd="mypassword"
          database = "database"
    )
    crsr = connection.cursor()
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM
                profileRecValues WHERE user_id = '%d'""" % currentUser)
    userData = crsr.fetchall()
    crsr.execute("""SELECT age_low, age_high, price, gender1, gender2, toiletries,
                clothes, homeware, entertainment, consumable, sport, other FROM
                productRecValues WHERE product_id = '%d'""" % recommendedProduct[0][0])
    productData = crsr.fetchall()
    userData = userData[0]
    productData = productData[0]
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
                SET age_low = ?, age_high = ?, price = ?, gender1 = ?, gender2 = ?, toiletries = ?,
                clothes = ?, homeware = ?, entertainment = ?, consumable = ?, sport = ?, other = ?
                WHERE user_id = ?""", (newUserValues[0], newUserValues[1], newUserValues[2],
                newUserValues[3], newUserValues[4], newUserValues[5], newUserValues[6],
                newUserValues[7], newUserValues[8], newUserValues[9], newUserValues[10],
                newUserValues[11], currentUser))
    crsr.execute("""UPDATE productRecValues
                SET age_low = ?, age_high = ?, price = ?, gender1 = ?, gender2 = ?, toiletries = ?,
                clothes = ?, homeware = ?, entertainment = ?, consumable = ?, sport = ?, other = ?
                WHERE product_id = ?""", (newProductValues[0], newProductValues[1], newProductValues[2],
                newProductValues[3], newProductValues[4], newProductValues[5], newProductValues[6],
                newProductValues[7], newProductValues[8], newProductValues[9], newProductValues[10],
                newProductValues[11], recommendedProduct[0][0]))
    connection.commit()
    connection.close()

##########################################################################################
#TESTING
##########################################################################################

#Generate database
try:
    createDB()
except:
    pass

#Add extra required tables
try:
    initialise()
except:
    pass

#Checks for extra products added
update()

#Produce sample current user
connection = sqlite3.connect("database.db")
crsr = connection.cursor()
crsr.execute("SELECT * FROM users WHERE user_id = 1")
currentUser = crsr.fetchall()
currentUser = currentUser[0][0]

#Perform action on load
alreadyRecc = onLoad()
#Produces suggestions and update accordingly
while(True == True):
    recommendedProduct = Recommendation(currentUser, alreadyRecc)
    alreadyRecc = updateAlreadyRecc(recommendedProduct, alreadyRecc)
    result = IO(recommendedProduct)
    updateValues(result, recommendedProduct, currentUser)

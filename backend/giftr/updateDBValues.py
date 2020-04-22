##########################################################################################
#SHOULD BE RUN WHENEVER ITEMS ADDED TO DATABASE POPULATES DATABASE 
##########################################################################################
from giftr import app, mysql
from flask import Flask, redirect, url_for, render_template, request, session, make_response
from flask_mysqldb import MySQLdb
import ssl, hashlib, re, datetime, smtplib

def update():
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
    
update()

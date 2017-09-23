from flask import Flask, request, url_for, redirect, render_template
<<<<<<< HEAD
import urllib
=======
#from flask_googlemaps import GoogleMaps

import urllib.request
>>>>>>> 81a2e9bf79b3a7f06177e8e6ce89105cf4503fd1
import json
import requests
import codecs
import sqlite3
import geopy
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import xml.etree.ElementTree as ET
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
#import twiliocall

app = Flask(__name__)

<<<<<<< HEAD
def initialize():
    url = "https://api.myjson.com/bins/10fryj"
    data = urllib.urlopen(url)
    reader = codecs.getreader('utf-8')
    trees = json.load(reader(data))

    conn = sqlite3.connect('hack1.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS People;
        CREATE TABLE People (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name   TEXT UNIQUE,
        num    TEXT UNIQUE,
        location TEXT UNIQUE 
    )''')

    for tree in trees:
        name = tree['name']
        num = tree['num']
        location = tree['location']
        cur.execute('''INSERT OR IGNORE INTO People (name,num,location) 
        VALUES ( ? , ? , ? )''', ( name,num,location ) )
        conn.commit()
    return

initialize()

def twil(num):
    account_sid = 'ACed10e34bac3a56da30b364c7eb639799'
    auth_token = 'f04d7af9f40effaceb83d1b6f2946a62'

    client = Client(account_sid,auth_token)

    client.messages.create(
        to = num,
        from_ = "+13475149453",
        body = "SOS. Help needed at link. Reply 1 if you are willing to help. Reply 0 if you arent willing to help."
        )
    if str(num) == '+14122189595':
        return 0
    else: 
        return 1

# def json_msg(name,dist):

#     data = '''
#     {
#     "name" : "%s",
#     "dist" : "%s"
#     }'''%(name,dist)

#     info = json.loads(data)
#     return info

def smallest():
    conn = sqlite3.connect('hack1.sqlite')
    cursor = conn.cursor()
    table = cursor.execute("SELECT * FROM People;")

    nearest = None
    curr = None
    thisname = None
    thisnum = None

    rows = 0
    for row in table:
        rows += 1
    print(rows)
    for i in range (1,rows+1):
        cursor.execute('''SELECT max(id) FROM People''')
        i = cursor.fetchone()[0]

        cursor.execute('''SELECT name FROM People WHERE id = (?)''',(i,))
        name = cursor.fetchone()[0]
        #print(name)
        #print name
        cursor.execute('''SELECT num FROM People WHERE id = (?)''',(i,))
        num = cursor.fetchone()[0]
        #print num

        cursor.execute('''SELECT location FROM People WHERE id = (?)''',(i,))
        location = cursor.fetchone()[0]
        #print location

        loc = Nominatim().geocode(location)
        row_loc = (loc.latitude, loc.longitude)

        #print(lat_lon_sos)
        dist = vincenty(lat_lon_sos, row_loc).miles
<<<<<<< HEAD
        print(nearest == None)
        print(name)
        if dist < nearest or nearest == None:
            print(dist)
            print(nearest)
=======
        #print(dist)
        if nearest == None or dist < nearest:
>>>>>>> 81a2e9bf79b3a7f06177e8e6ce89105cf4503fd1
            nearest = dist
            print(nearest)
            print('\n')
            thisname = name
            thisnum = num
            #print(nearest)
            place = curr
            back.append([name,num,location])

    cursor.execute(''' DELETE FROM People WHERE name = ( ? )''', (thisname, )) 
    conn.commit()
    #print(thisname,nearest)
    #result = json_msg(thisname,nearest)
    print(thisnum+"thisnum")
    return twil(thisnum)
    
def sending():
    first = smallest()
    second = smallest()

    while True:
        if first != 1 and second != 1:
            first = smallest()
            second = smallest()
        elif first != 1 and second == 1:
            first = smallest()
        if first == 1 and second != 1:
            second = smallest()
        else:
            break

    conny = sqlite3.connect('hack1.sqlite')
    curry = conny.cursor()
    for item in back:
        curry.execute('''INSERT OR IGNORE INTO People (name,num,location) 
        VALUES ( ? , ? , ? )''', (item[0],item[1],item[2] ) )

=======
>>>>>>> 6fe9c50aa5deaa7206f06d11e71f75a48ba4eaf2
@app.route('/')
def index():
    author = "Me"
    name = "Jihyun"
    return render_template('index.html', author=author, name=name)

@app.route('/urgent', methods=['GET', 'POST'])
def urgent_btn():
	#os.system('python twiliocall.py')
	if request.method == 'POST':
		return redirect(url_for('index'))

	return render_template('urgent.html')

@app.route('/danger', methods=['GET', 'POST'])
def danger_btn():
	if request.method == 'POST':
		return redirect(url_for('index'))
	return render_template('danger.html')

@app.route('/safewalk', methods=['GET', 'POST'])
def safewalk_btn():
	if request.method == 'POST':
		return redirect(url_for('index'))
	return render_template('safewalk.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit_btn():
	if request.method == 'POST':
		return redirect(url_for('index'))
	return render_template('urgent.html')

@app.route('/done', methods=['GET', 'POST'])
def safe_submit_btn():
	if request.method == 'POST':
		return redirect(url_for('index'))
	return render_template('safewalk_res.html')

@app.route('/done!', methods=['GET', 'POST'])
def danger_submit_btn():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('danger_res.html')



if __name__ == "__main__":
    app.run(debug=True)


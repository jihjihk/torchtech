#ADD LI'S NUMBER 
#make sure return is working, its a json file
import urllib
import json
import requests
import sqlite3
import geopy
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import xml.etree.ElementTree as ET
import os
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

back = list()

freegeoip = "http://freegeoip.net/json"
geo_r = requests.get(freegeoip)
geo_json = geo_r.json()

user_position = [geo_json["latitude"], geo_json["longitude"]]
lat_lon_sos = (user_position[0], user_position[1])

result = None

def initialize():
    url = "https://api.myjson.com/bins/10fryj"


    data = urllib.urlopen(url)
    trees = json.load(data)

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

def json_msg(name,dist):

    data = '''
    {
    "name" : "%s",
    "dist" : "%s"
    }'''%(name,dist)

    info = json.loads(data)
    return info

def smallest():
    conn = sqlite3.connect('hack1.sqlite')
    cursor = conn.cursor()
    table = cursor.execute("SELECT * FROM People;")

    nearest = None
    curr = None
    thisname = None
    thisnum = None

    maxId = None
    custId = None

    rows = 0
    for row in table:
        rows += 1
    for i in range (1,rows+1):
        cursor.execute('''SELECT max(id) FROM People''')
        i = cursor.fetchone()[0]

        cursor.execute('''SELECT name FROM People WHERE id = (?)''',(i,))
        name = cursor.fetchone()[0]
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
        #print(dist)
        if dist < nearest or nearest == None:
            nearest = dist
            thisname = name
            thisnum = num
            #print(nearest)
            place = curr
            back.append([name,num,location])
    cursor.execute(''' DELETE FROM People WHERE name = ( ? )''', (thisname, )) 
    conn.commit()
    #print(thisname,nearest)
    result = json_msg(thisname,nearest)
    #print(thisnum)
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

sending()
return (result)

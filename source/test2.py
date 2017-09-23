from flask import Flask, request, redirect
import urllib
import json
import codecs
import sqlite3
import geopy
import requests
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import xml.etree.ElementTree as ET
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

def initialize():
    url = "https://api.myjson.com/bins/hkjsr"
    data = urllib.urlopen(url).read()
    trees = json.loads(data)

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

def twil(num,user_add):
    account_sid = 'ACed10e34bac3a56da30b364c7eb639799'
    auth_token = 'f04d7af9f40effaceb83d1b6f2946a62'

    client = Client(account_sid,auth_token)

    client.messages.create(
        to = num,
        from_ = "+13475149453",
        body = "SOS. Help needed at location : %s"%(user_add)
        )

    return 1 #see if person said yes or no later

def smallest(back):

    freegeoip = "http://freegeoip.net/json"
    geo_r = requests.get(freegeoip)
    geo_json = json.loads(geo_r.text)

    user_position = [geo_json["latitude"], geo_json["longitude"]]
    lat_lon_sos = (user_position[0], user_position[1])
    user_add = Nominatim().reverse(lat_lon_sos)

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
    
    for i in range (1,rows+1):
        cursor.execute('''SELECT max(id) FROM People''')
        i = cursor.fetchone()[0]

        cursor.execute('''SELECT name FROM People WHERE id = (?)''',(i,))
        name = cursor.fetchone()[0]

        cursor.execute('''SELECT num FROM People WHERE id = (?)''',(i,))
        num = cursor.fetchone()[0]

        cursor.execute('''SELECT location FROM People WHERE id = (?)''',(i,))
        location = cursor.fetchone()[0]

        loc = Nominatim().geocode(location)
        row_loc = (loc.latitude, loc.longitude)

        dist = vincenty(lat_lon_sos, row_loc).miles

        if nearest == None or dist < nearest:
            nearest = dist
            thisname = name
            thisnum = num
            place = curr
            back.append([name,num,location])

    cursor.execute(''' DELETE FROM People WHERE name = ( ? )''', (thisname, )) 
    conn.commit()
    return twil(thisnum,user_add)
    
def sending():
    back = list()
    first = smallest(back)

    while True:
        if first != 1:
            first = smallest()
        else:
            break

    conny = sqlite3.connect('hack1.sqlite')
    curry = conny.cursor()
    for item in back:
        curry.execute('''INSERT OR IGNORE INTO People (name,num,location) 
        VALUES ( ? , ? , ? )''', (item[0],item[1],item[2] ) )


def main():
    initialize()
    sending()


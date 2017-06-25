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


freegeoip = "http://freegeoip.net/json"
geo_r = requests.get(freegeoip)
geo_json = geo_r.json()

user_position = [geo_json["latitude"], geo_json["longitude"]]
lat_lon_sos = (user_position[0], user_position[1])


conn = sqlite3.connect('hack1.sqlite')
cursor = conn.cursor()
table = cursor.fetchall()


app = Flask(__name__)
@app.route("/sms", methods = ['GET','POST'])

def sms_reply():
    resp = MessagingResponse()
    resp.message("Thank you")
    return str(resp)

def twil(num):
    account_sid = 'ACed10e34bac3a56da30b364c7eb639799'
    auth_token = 'f04d7af9f40effaceb83d1b6f2946a62'

    client = Client(account_sid,auth_token)

    client.messages.create(
        to = num,
        from_ = "+13475149453",
        body = "SOS. Help needed at link. Reply 1 if you are willing to help. Reply 0 if you arent willing to help."
        )
    return int(sms_reply())

def json_msg(name,dist):

    data = '''
    {
    "name" : "%s",
    "dist" : "%s"
    }'''%(name,dist)

    info = json.loads(data)
    return info

back = list()
def smallest():
    place = None
    nearest = None
    name = None
    num = None
    for row in table:
        name = cursor.executescript('''SELECT name FROM row''')
        num = cursor.executescript('''SELECT num FROM row''')

        location = cursor.executescript('''SELECT location FROM row''')
        loc = Nominatim().geocode(location)
        row_loc = (loc.latitude, loc.longitude)

        dist = vincenty(lat_lon_sos, row_loc).miles
        if dist < nearest:
            nearest = dist
            place = curr
            back.append([name,num,location])
    cursor.executescript(''' DELETE FROM People WHERE location = ( ? )''', (place,)) 
    json_msg(name,nearest)
    return twil(num)
    

conn.close()

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

    for item in back:
        cur.execute('''INSERT OR IGNORE INTO People (name,num,location) 
        VALUES ( ? )''', (item[0],item[1],item[2] ) )
        





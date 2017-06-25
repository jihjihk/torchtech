import urllib
import json
import sqlite
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import xml.etree.ElementTree as ET
import os
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import messaging_response


while True:
    if len(url)<1: break

    freegeoip = "http://freegeoip.net/json"
    geo_r = requests.get(freegeoip)
    geo_json = geo_r.json()

    user_postition = [geo_json["latitude"], geo_json["longitude"]]
    lat_lon_sos = (user_position[0], user_position[1])

    
    conn = sqlite.connect('hack1.sqlite')
    cursor = conn.cursor()
    table = cursor.fetchall()

    
    def twil(num):
        account_sid = 
        auth_token = 

        client = Client(account_sid,auth_token)

        client.messages.create(
            to = num,
            from_ = "purchased num",
            body = "SOS. Help needed at link. Reply 1 if you are willing to help. Reply 0 if you arent willing to help."
            )

        
        app = Fask(__name__)

        @app.route("/sms", method = ['GET','POST'])
        resp = MessagingResponse()
        resp.message("Thank you")
        return int(resp)

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
        third = smallest()

        while True:
            if first != 1 and second != 1 and third != 1: 
                first = smallest()
                second = smallest()
                third = smallest()
            elif first ==1 and second != 1 and third != 1:
                second = smallest()
                third = smallest()
            elif first !=1 and second == 1 and third != 1:
                first = smallest()
                third = smallest()
            elif first !=1 and second != 1 and third == 1:
                second = smallest()
                first = smallest()
            elif first !=1 and second == 1 and third == 1:
                first = smallest()
            elif first ==1 and second != 1 and third == 1:
                second = smallest()
            elif first ==1 and second = 1 and third != 1:
                third = smallest()
            else:
                break

        for item in back:
            cur.execute('''INSERT OR IGNORE INTO People (name,num,location) 
            VALUES ( ? )''', (item[0],item[1],item[2] ) )
            
    



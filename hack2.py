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


url = #same link each time, add that link here 
while True:
    if len(url)<1: break

    data = urllib.urlopen(url)
    tree = json.load(data)
    sos = tree['sos']
    
    location_sos = Nominatim().geocode(sos)
    lat_lon_sos = (location_sos.latitude, location_sos.longitude)

    
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
            body = "SOS. Help needed at link"
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
        cursor.executescript(''' DELETE FROM People WHERE location = ( ? )''', (place,)) #add back after you have found three people
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

    




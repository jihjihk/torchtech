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
import codecs
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

def initialize():
    url = "https://api.myjson.com/bins/10fryj"
    data = urllib.request.urlopen(url).read().decode('utf-8')
    #reader = codecs.getreader('utf-8')
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

def twil(num):
    account_sid = 'ACed10e34bac3a56da30b364c7eb639799'
    auth_token = 'f04d7af9f40effaceb83d1b6f2946a62'

    client = Client(account_sid,auth_token)

    client.messages.create(
        to = num,
        from_ = "+13475149453",
        body = "SOS. Help needed at link. Reply 1 if you are willing to help. Reply 0 if you arent willing to help."
        )

def smallest():
    conn = sqlite3.connect('hack1.sqlite')
    cursor = conn.cursor()
    table = cursor.execute("SELECT * FROM People;")

    rows = 0
    for row in table:
        rows += 1
    
    for i in range (1,rows+1):
        cursor.execute('''SELECT num FROM People WHERE id = (?)''',(i,))
        num = cursor.fetchone()[0]
        twil(num)
    

def main():
    initialize()
    smallest()
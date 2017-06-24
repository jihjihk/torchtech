import urllib
import json
import sqlite
import xml.etree.ElementTree as ET

url = #same link each time, add that link here 
while True:
    if len(url)<1: break

    data = urllib.urlopen(url)
    tree = json.load(data)
    name = tree['name']
    numb = tree['number']
    location = tree['location']
    
    conn = sqlite3.connect('hack1.sqlite')
    cur = conn.cursor()

    cur.executescript('''

    CREATE TABLE IF NOT EXISTS People (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name   TEXT UNIQUE,
        num    TEXT UNIQUE,
        location TEXT UNIQUE 
        );
    ''')

    cur.execute('''INSERT OR IGNORE INTO People (name) 
        VALUES ( ? )''', ( name, ) )
    cur.execute('''INSERT OR IGNORE INTO People (num)
        VALUES ( ? )''', ( num, ) )
    cur.execute('''INSERT OR IGNORE INTO People (location)
        VALUES ( ? )''', ( location, ) )
    conn.commit()
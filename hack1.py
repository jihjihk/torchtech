import urllib
import json
import sqlite3
import xml.etree.ElementTree as ET

url = "https://api.myjson.com/bins/erd1v"


data = urllib.urlopen(url)
trees = json.load(data)

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

for tree in trees:
    name = tree['name']
    num = tree['num']
    location = tree['location']

    cur.execute('''INSERT OR IGNORE INTO People (name,num,location) 
    VALUES ( ? , ? , ? )''', ( name,num,location ) )

    conn.commit()
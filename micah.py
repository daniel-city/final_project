import requests
import sqlite3
import time
import json

api_key = "823ebf192a9537ddb2cbb92ea29ff225"
coords = [(40.7580, -73.9855), (37.7749, -122.4194), (41.8837, -87.6315), (42.2776, -83.7409), (34.0522, -118.2437)]

def get_walkscore(lat, lon):
    url = f"https://api.walkscore.com/score?format=json&lat={lat}&lon={lon}&transit=1&bike=1&wsapikey={api_key}"
    r = requests.get(url)
    try:
        r.raise_for_status()
        return r.json()
    except:
        return None

conn = sqlite3.connect("walkscore.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS locations (id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    UNIQUE(latitude, longitude));""")

cur.execute("""CREATE TABLE IF NOT EXISTS walkscore_results (id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    walkscore INTEGER,
    description TEXT,
    transit_score INTEGER,
    bike_score INTEGER,
    UNIQUE(location_id),
    FOREIGN KEY(location_id) REFERENCES locations(id));""")

conn.commit()
for lat, lon in coords:
    cur.execute("""INSERT OR IGNORE INTO locations (latitude, longitude) VALUES (?, ?);""", (lat, lon))
    conn.commit()
    
    cur.execute("""SELECT id FROM locations WHERE latitude=? AND longitude=?""", (lat, lon))
    location_id = cur.fetchone()[0]
    
    cur.execute("""SELECT 1 FROM walkscore_results WHERE location_id=?""", (location_id,))
    if cur.fetchone():
        continue

    data = get_walkscore(lat, lon)
    if not data or data.get("status") != 1:
        print(f"No usable data for {lat}, {lon}")
        continue

    cur.execute("""INSERT INTO walkscore_results (location_id, walkscore, description, transit_score, bike_score) VALUES (?, ?, ?, ?, ?)""", (
        location_id,
        data.get("walkscore"),
        data.get("description"),
        data.get("transit", {}).get("score"),
        data.get("bike", {}).get("score"),))
    conn.commit()
    time.sleep(1)

conn.close()

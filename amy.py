import json
import sqlite3
import os
import requests

API_KEY = "bd1842990d39e66f7830f18d756cb443636008b7"

top_cities_file = "top100_cities.json"
raw_json_file = "aqi_data.json"
db_file = "air_quality.db"

batch_size = 25

def load_top_cities():
    if not os.path.exists(top_cities_file):
        raise FileNotFoundError(f"{top_cities_file} not found.")
    with open(top_cities_file, "r") as f:
        return json.load(f)
    

def init_db():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    #cities table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        country TEXT,
        lat REAL,
        lon REAL
    )
    """)

    #AQI readings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS AQIReadings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER,
            aqi INTEGER,
            dominentpol TEXT,
            time_utc TEXT,
            pm25 REAL,
            pm10 REAL,
            o3 REAL,
            no2 REAL,
            so2 REAL,
            co REAL,
            raw_json TEXT,
            FOREIGN KEY(city_id) REFERENCES Cities(id)
        )
    """)

    conn.commit()
    return conn, cur

def fetch_aqi(lat, lon):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
    params = {"token": API_KEY}

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            return None
        return data
    except:
        return None
    
def get_top_cities_aqi():
    cities = load_top_cities()
    conn, cur, init_db()

    if os.path.exists(raw_json_file):
        try:
            with open(raw_json_file, "r") as f:
                raw_json_data = json.load(f)
        except:
            raw_json_data = []
    else:
        raw_json_data = []

    cur.execute("SELECT name FROM Cities")
    existing_cities = set(row[0] for row in cur.fetchall())

    added = 0

    for city in cities:
        if added >= batch_size:
            break
        name = city["name"]
        if name in existing_cities:
            continue

        print("Getting AQI for:", name)
        data = fetch_aqi(city["lat"], city["lon"])

        if data is None:
            print("  Failed to get data for:", name)
            continue

        raw_json_data.append({
            "city": name,
            "country": city["country"],
            "lat": city["lat"],
            "lon": city["lon"],
            "api_response": data
        })

        with open(raw_json_file, "w") as f:
            json.dump(raw_json_data, f, indent=2)

        # Insert city
        cur.execute("""
            INSERT OR IGNORE INTO Cities (name, country, lat, lon)
            VALUES (?, ?, ?, ?)
        """, (name, city["country"], city["lat"], city["lon"]))
        conn.commit()

        cur.execute("SELECT id FROM Cities WHERE name = ?", (name,))
        city_id = cur.fetchone()[0]

        #pollutants
        d = data.get("data", {})
        iaqi = d.get("iaqi", {})

        def val(key):
            if key in iaqi and isinstance(iaqi[key], dict):
                return iaqi[key].get("v")
            return None
        
        #insert AQI
        cur.execute("""
            INSERT INTO AQIReadings (
                city_id, aqi, dominentpol, time_utc,
                pm25, pm10, o3, no2, so2, co, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            city_id,
            d.get("aqi"),
            d.get("dominentpol"),
            d.get("time", {}).get("iso"),
            val("pm25"),
            val("pm10"),
            val("o3"),
            val("no2"),
            val("so2"),
            val("co"),
            json.dumps(data)
        ))

        conn.commit()
        added += 1
        existing_cities.add(name)
        print("  Added AQI for:", name)

    print("Finished batch:", added, "new cities.")
    conn.close()
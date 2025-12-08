import json
import sqlite3
import os
import requests

amy_key = "bd1842990d39e66f7830f18d756cb443636008b7"

top_cities_file = "top100_cities.json"
raw_json_file = "aqi_data.json"
db_file = "air_quality.db"

batch_size = 25

coordinates = [
    '40.7128,-74.0060',    # New York, NY
    '34.0522,-118.2437',   # Los Angeles, CA
    '41.8781,-87.6298',    # Chicago, IL
    '29.7604,-95.3698',    # Houston, TX
    '33.4484,-112.0740',   # Phoenix, AZ
    '39.9526,-75.1652',    # Philadelphia, PA
    '29.4241,-98.4936',    # San Antonio, TX
    '32.7157,-117.1611',   # San Diego, CA
    '32.7767,-96.7970',    # Dallas, TX
    '37.3382,-121.8863',   # San Jose, CA
    '30.2672,-97.7431',    # Austin, TX
    '30.3322,-81.6557',    # Jacksonville, FL
    '32.7555,-97.3308',    # Fort Worth, TX
    '39.9612,-82.9988',    # Columbus, OH
    '35.2271,-80.8431',    # Charlotte, NC
    '37.7749,-122.4194',   # San Francisco, CA
    '39.7684,-86.1581',    # Indianapolis, IN
    '47.6062,-122.3321',   # Seattle, WA
    '39.7392,-104.9903',   # Denver, CO
    '38.9072,-77.0369',    # Washington, DC
    '42.3601,-71.0589',    # Boston, MA
    '31.7619,-106.4850',   # El Paso, TX
    '36.1627,-86.7816',    # Nashville, TN
    '42.3314,-83.0458',    # Detroit, MI
    '35.4676,-97.5164',    # Oklahoma City, OK
    '45.5051,-122.6750',   # Portland, OR
    '36.1699,-115.1398',   # Las Vegas, NV
    '35.1495,-90.0490',    # Memphis, TN
    '38.2527,-85.7585',    # Louisville, KY
    '39.2904,-76.6122',    # Baltimore, MD
    '43.0389,-87.9065',    # Milwaukee, WI
    '35.0844,-106.6504',   # Albuquerque, NM
    '32.2226,-110.9747',   # Tucson, AZ
    '36.7378,-119.7871',   # Fresno, CA
    '38.5816,-121.4944',   # Sacramento, CA
    '33.4152,-111.8315',   # Mesa, AZ
    '33.7490,-84.3880',    # Atlanta, GA
    '41.2565,-95.9345',    # Omaha, NE
    '38.8339,-104.8214',   # Colorado Springs, CO
    '35.7796,-78.6382',    # Raleigh, NC
    '36.8529,-75.9780',    # Virginia Beach, VA
    '25.7617,-80.1918',    # Miami, FL
    '33.7701,-118.1937',   # Long Beach, CA
    '37.8044,-122.2711',   # Oakland, CA
    '44.9778,-93.2650',    # Minneapolis, MN
    '39.1031,-84.5120',    # Cincinnati, OH
    '43.0731,-89.4012',    # Madison, WI
    '35.0456,-85.3097',    # Chattanooga, TN
    '39.7397,-75.5390',    # Camden, NJ
    '32.6781,-83.2220',    # Augusta, GA
    '29.9511,-90.0715',    # New Orleans, LA
    '36.1745,-86.7670',    # Nashville, TN (duplicate removed later)
    '30.6954,-88.0399',    # Mobile, AL
    '39.9610,-82.9988',    # Columbus, OH (duplicate removed later)
    '40.4406,-79.9959',    # Pittsburgh, PA
    '43.6532,-79.3832',    # Toronto, ON (optional non-US)
    '40.7357,-74.1724',    # Newark, NJ
    '39.9612,-82.9988',    # Columbus, OH (duplicate)
    '42.1015,-72.5898',    # Springfield, MA
    '36.1627,-86.7816',    # Nashville, TN (duplicate)
    '33.5207,-86.8025',    # Birmingham, AL
    '29.4241,-98.4936',    # San Antonio, TX (duplicate)
    '32.7765,-79.9311',    # Charleston, SC
    '38.6270,-90.1994',    # St. Louis, MO
    '35.2271,-80.8431',    # Charlotte, NC (duplicate)
    '35.1495,-90.0490',    # Memphis, TN (duplicate)
    '36.0972,-79.7745',    # Greensboro, NC
    '40.7306,-73.9352',    # Queens, NY
    '39.7684,-86.1581',    # Indianapolis, IN (duplicate)
    '41.6005,-93.6091',    # Des Moines, IA
    '36.7783,-119.4179',   # California (approximate center)
    '40.6501,-73.9496',    # Brooklyn, NY
    '33.4484,-112.0740',   # Phoenix, AZ (duplicate)
    '34.0007,-81.0348',    # Columbia, SC
    '42.3314,-83.0458',    # Detroit, MI (duplicate)
    '30.3322,-81.6557',    # Jacksonville, FL (duplicate)
    '39.9612,-82.9988',    # Columbus, OH (duplicate)
    '38.5816,-121.4944',   # Sacramento, CA (duplicate)
    '36.7468,-119.7726',   # Fresno, CA (duplicate)
    '40.4406,-79.9959',    # Pittsburgh, PA (duplicate)
    '42.3601,-71.0589',    # Boston, MA (duplicate)
    '39.7684,-86.1581',    # Indianapolis, IN (duplicate)
    '32.7555,-97.3308',    # Fort Worth, TX (duplicate)
    '30.2672,-97.7431',    # Austin, TX (duplicate)
    '32.7157,-117.1611',   # San Diego, CA (duplicate)
    '47.6062,-122.3321',   # Seattle, WA (duplicate)
    '39.7392,-104.9903',   # Denver, CO (duplicate)
    '38.9072,-77.0369',    # Washington, DC (duplicate)
    '34.0522,-118.2437',   # Los Angeles, CA (duplicate)
    '40.7128,-74.0060'     # New York, NY (duplicate)
]

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
    amy_url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
    params = {"token": amy_key}

    try:
        response = requests.get(amy_url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            return None
        return data
    except:
        return None
    
def get_top_cities_aqi():
    conn, cur, init_db()

    if os.path.exists(raw_json_file):
        try:
            with open(raw_json_file, "r") as f:
                raw_json_data = json.load(f)
        except:
            raw_json_data = []
    else:
        raw_json_data = []

    cur.execute("SELECT COUNT(*) FROM aqi_results")
    completed = cur.fetchone()[0]

    next_coords = coords[completed: completed + batch_size]

    added = 0

    for lat, lon in next_coords:
        print("Getting AQI for:", lat, lon)
         
        cur.executre("""
            INSERT OR IGNORE INTO locations (latitude, longitude)
            VALUES (?, ?)
        """, (lat, lon))
        conn.commit()

        cur.execute("""
            SELECT id FROM locations
            WHERE latitude = ? AND longitude = ?
        """, (lat, lon))
        loc_row = cur.fetchone()
        if not loc_row:
            print("  Failed to insert location:", lat, lon)
            continue

        loc_id = loc_row[0]

        cur.execute("SELECT 1 FROM aqi_results WHERE location_id = ?", (loc_id,)
        if cur.fetchone():
            print("  AQI already exists for this location.")
            continue

        data = fetch_aqi(lat, lon)
        if data is None:
            print("  Failed to fetch AQI data.")
            continue
            
        raw_json_data.append({
            "latitude": lat,
            "longitude": lon,
            "api_response": data
        }

        with open(raw_json_file, "w") as f:
            json.dump(raw_json_data, f, indent=2)

        d = data.get("data", {})
        iaqi = d.get("iaqi", {})

        def val(k):
            if k in iaqi and isinstance(iaqi[k], dict):
                return iaqi[k].get("v")
            return None
        
        cur.execute("""
            INSERT INTO aqi_results (
                location_id, aqi, dominentpol, time_utc,
                pm25, pm10, o3, no2, so2, co, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            location_id,
            d.get("aqi"),
            d.get("dominentpol"),
            d.get("time", {}).get("iso"),
            val("pm25"), val("pm10"), val("o3"), val("no2"),
            val("so2"), val("co"),
            json.dumps(data)
        ))

        conn.commit()
        added += 1
        print("  Added AQI entry.")

    print("\nFinished. Added:", added, "new AQI entries.")
    conn.close()

import requests
import sqlite3
import time
import json
import os
import matplotlib.pyplot as plt

# MICAH'S API KEY

micah_api_key = "823ebf192a9537ddb2cbb92ea29ff225"

# DANIEL'S API KEY AND COORDINATES

daniel_api_key = "rwB7lgYNsAsKDJupv7fHFd8MXaHuK8TQ"
coordinate_points = [
    "40.7128,-74.0060",  # New York, NY
    "34.0522,-118.2437",  # Los Angeles, CA
    "41.8781,-87.6298",  # Chicago, IL
    "29.7604,-95.3698",  # Houston, TX
    "33.4484,-112.0740",  # Phoenix, AZ
    "39.9526,-75.1652",  # Philadelphia, PA
    "29.4241,-98.4936",  # San Antonio, TX
    "32.7157,-117.1611",  # San Diego, CA
    "32.7767,-96.7970",  # Dallas, TX
    "37.3382,-121.8863",  # San Jose, CA
    "30.2672,-97.7431",  # Austin, TX
    "30.3322,-81.6557",  # Jacksonville, FL
    "32.7555,-97.3308",  # Fort Worth, TX
    "39.9612,-82.9988",  # Columbus, OH
    "35.2271,-80.8431",  # Charlotte, NC
    "37.7749,-122.4194",  # San Francisco, CA
    "39.7684,-86.1581",  # Indianapolis, IN
    "47.6062,-122.3321",  # Seattle, WA
    "39.7392,-104.9903",  # Denver, CO
    "38.9072,-77.0369",  # Washington, DC
    "42.3601,-71.0589",  # Boston, MA
    "31.7619,-106.4850",  # El Paso, TX
    "36.1627,-86.7816",  # Nashville, TN
    "42.3314,-83.0458",  # Detroit, MI
    "35.4676,-97.5164",  # Oklahoma City, OK
    "45.5051,-122.6750",  # Portland, OR
    "36.1699,-115.1398",  # Las Vegas, NV
    "35.1495,-90.0490",  # Memphis, TN
    "38.5816,-121.4944",  # Sacramento, CA
    "38.2527,-85.7585",  # Louisville, KY
    "39.2904,-76.6122",  # Baltimore, MD
    "43.0389,-87.9065",  # Milwaukee, WI
    "35.0844,-106.6504",  # Albuquerque, NM
    "36.7378,-119.7871",  # Fresno, CA
    "32.2226,-110.9747",  # Tucson, AZ
    "41.2565,-95.9345",  # Omaha, NE
    "38.8339,-104.8214",  # Colorado Springs, CO
    "36.8529,-75.9780",  # Virginia Beach, VA
    "35.7796,-78.6382",  # Raleigh, NC
    "25.7617,-80.1918",  # Miami, FL
    "43.6532,-79.3832",  # Toronto, ON
    "45.5017,-73.5673",  # Montreal, QC
    "49.2827,-123.1207",  # Vancouver, BC
    "51.0447,-114.0719",  # Calgary, AB
    "53.5461,-113.4938",  # Edmonton, AB
    "45.4215,-75.6972",  # Ottawa, ON
    "43.5890,-79.6441",  # Mississauga, ON
    "49.8951,-97.1384",  # Winnipeg, MB
    "44.6488,-63.5752",  # Halifax, NS
    "43.4501,-80.4832",  # Kitchener, ON
    "45.4112,-75.6981",  # Gatineau, QC
    "52.2681,-113.8112",  # Red Deer, AB
    "50.4452,-104.6189",  # Regina, SK
    "53.9140,-122.7497",  # Prince George, BC
    "43.2557,-79.8711",  # Hamilton, ON
    "43.1610,-79.2440",  # St. Catharines, ON
    "42.8864,-78.8784",  # Buffalo, NY
    "27.9506,-82.4572",  # Tampa, FL
    "40.4406,-79.9959",  # Pittsburgh, PA
    "39.1031,-84.5120",  # Cincinnati, OH
    "41.4993,-81.6944",  # Cleveland, OH
    "44.9778,-93.2650",  # Minneapolis, MN
    "29.9511,-90.0715",  # New Orleans, LA
    "33.5207,-86.8025",  # Birmingham, AL
    "32.3513,-95.3011",  # Tyler, TX
    "45.0275,-93.3655",  # Brooklyn Park, MN
    "30.4383,-84.2807",  # Tallahassee, FL
    "33.7488,-84.3880",  # Atlanta, GA
    "34.0007,-81.0348",  # Columbia, SC
    "21.3069,-157.8583",  # Honolulu, HI
    "47.2529,-122.4443",  # Tacoma, WA
    "40.7608,-111.8910",  # Salt Lake City, UT
    "39.0997,-94.5786",  # Kansas City, MO
    "33.6846,-117.8265",  # Irvine, CA
    "35.3733,-119.0187",  # Bakersfield, CA
    "30.6954,-88.0399",  # Mobile, AL
    "40.0140,-105.2705",  # Boulder, CO
    "43.0481,-76.1474",  # Syracuse, NY
    "39.5296,-119.8138",  # Reno, NV
    "32.7765,-79.9311",  # Charleston, SC
    "40.8258,-74.2090",  # Newark, NJ
    "33.3062,-111.8413",  # Chandler, AZ 
    "41.6639,-83.5552",  # Toledo, OH 
    "44.9537,-93.0900",  # St. Paul, MN 
    "26.0078,-80.2963",  # Pembroke Pines, FL 
    "42.6526,-73.7562",  # Albany, NY
    "45.2733,-66.0633",  # Saint John, NB
    "52.8390,-104.6060",  # Melfort, SK
    "35.9940,-78.8986",  # Durham, NC
    "37.5407,-77.4360",  # Richmond, VA
]


daniel_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

one_hundred_data = []

for coordinate in coordinate_points:
    params = {
        'key': daniel_api_key,
        'point': coordinate,
    }
    response = requests.get(daniel_url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            data["coordinates input"] = coordinate
            one_hundred_data.append(data)
            #print(data)
        except requests.exceptions.JSONDecodeError:
            print("Response:", response.text)
    else:
        print(f"Error:  + {response.status_code}")

with open("traffic_flow_data.json", "w") as f:
    json.dump(one_hundred_data, f, indent=4)

full_path = os.path.join(os.path.dirname(__file__), "traffic_flow_data.json")
f = open(full_path)
file_data = f.read()
f.close()
json_data = json.loads(file_data)

# MICAH SQL CODE

def get_walkscore(lat, lon):
    url = f"https://api.walkscore.com/score?format=json&lat={lat}&lon={lon}&transit=1&bike=1&wsapikey={micah_api_key}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("ERROR:", e)
        return None


def create_SQL(conn):
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


def get_coords(conn, coords):
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM locations")
    already_done = cur.fetchone()[0]

    next_coords = coords[already_done:already_done + 25]

    for coord in next_coords:
        lat, lon = map(float, coord.split(','))
        cur.execute("""INSERT OR IGNORE INTO locations (latitude, longitude) VALUES (?, ?)""", (lat, lon))
        conn.commit()
        cur.execute("""SELECT id FROM locations WHERE latitude=? AND longitude=?""", (lat, lon))
        row = cur.fetchone()
        if not row:
            continue
        location_id = row[0]

        cur.execute("""SELECT 1 FROM walkscore_results WHERE location_id=?""", (location_id,))
        if cur.fetchone():
            continue

        data = get_walkscore(lat, lon)
        if not data or data.get("status") != 1:
            continue
        
        transit_score = data.get("transit", {}).get("score")
        bike_score = data.get("bike", {}).get("score")

        if transit_score is None:
            transit_score = 0
        if bike_score is None:
            bike_score = 0
        cur.execute("""INSERT INTO walkscore_results (location_id, walkscore, description, transit_score, bike_score) VALUES (?, ?, ?, ?, ?)""",
        (location_id, data.get("walkscore"), data.get("description"), transit_score, bike_score))
        conn.commit()
        time.sleep(1)


def num_description_and_visual(conn):
    cur = conn.cursor()
    cur.execute("SELECT description, COUNT(*) FROM walkscore_results GROUP BY description")
    results = cur.fetchall()

    descriptions = [desc for desc, count in results]
    counts = [count for desc, count in results]
    plt.figure(figsize=(10, 6))
    plt.barh(descriptions, counts, color="red")
    plt.xlabel("Number of Locations")
    plt.ylabel("Walk Score Description")
    plt.title("Number of Locations by Walk Score Description")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("walkscore_summary.png")
    plt.show()
    plt.close()
    return results


def calc_and_write(results):
    total = sum(count for category1, count in results)
    with open("outputs.txt", "w") as f:
        f.write(f"Total locations: {total}\n\n")
        for description, count in results:
            f.write(f"{description}: {count}\n")


def main():
    conn = sqlite3.connect("test.db")
    create_SQL(conn)
    get_coords(conn, coordinate_points)
    results = num_description_and_visual(conn)
    #conn.close()
    calc_and_write(results)


if __name__ == "__main__":
    main()

# DANIEL SQL CODE

db_name = "test.db"
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + db_name)
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS DanTrafficFlow
""")
conn.commit()
cur.execute("""
CREATE TABLE IF NOT EXISTS DanTrafficFlow (
id INTEGER PRIMARY KEY AUTOINCREMENT,
current_speed INTEGER,
freeflow_speed INTEGER,
current_travel_time INTEGER,
freeflow_travel_time INTEGER,
coordinates_id INTEGER NOT NULL,
FOREIGN KEY (coordinates_id) REFERENCES locations(id)
)
""")
conn.commit()

counter = 0

for location in json_data:
    current_speed = location["flowSegmentData"]["currentSpeed"]
    #print(current_speed)
    freeflow_speed = location["flowSegmentData"]["freeFlowSpeed"]
    current_travel_time = location["flowSegmentData"]["currentTravelTime"]
    freeflow_travel_time = location["flowSegmentData"]["freeFlowTravelTime"]
    latitude = coordinate_points[counter][:7]
    longitude = coordinate_points[counter][8:]

    cur.execute("""

    SELECT id FROM locations WHERE latitude = ? AND longitude = ?
    """, (latitude, longitude))
    coordinates_id = cur.fetchone()

    if coordinates_id:
        coordinates_id = coordinates_id[0]
    
        cur.execute("""
        INSERT OR IGNORE INTO DanTrafficFlow (current_speed, freeflow_speed, current_travel_time, freeflow_travel_time, coordinates_id)
        VALUES (?, ?, ?, ?, ?) """, (current_speed, freeflow_speed, current_travel_time, freeflow_travel_time, coordinates_id))

    counter += 1

conn.commit()

# for coordinate in coordinate_points:
#     latitude = coordinate[:9]
#     longitude = coordinate[10:]
#     cur.execute("""
#     INSERT OR IGNORE INTO TrafficFlow (latitude, longitude)
#     VALUES (?, ?) """, (latitude, longitude))

conn.commit()


# CONN CLOSE
#conn.close()

#amy code
amy_key = "bd1842990d39e66f7830f18d756cb443636008b7"

raw_json_file = "aqi_data.json"
db_file = "test.db"

batch_size = 25

def init_db():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # DO NOT DROP ANY TABLES HERE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        UNIQUE(latitude, longitude)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS aqi_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER NOT NULL,
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
        FOREIGN KEY(location_id) REFERENCES locations(id)
    );
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
    conn, cur = init_db()

    # load existing raw json cache
    if os.path.exists(raw_json_file):
        try:
            with open(raw_json_file, "r") as f:
                raw_json_data = json.load(f)
        except:
            raw_json_data = []
    else:
        raw_json_data = []

    added = 0

    for coord in coordinate_points:
        if added >= batch_size:
            break

        lat_str, lon_str = coord.split(',')
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())

        cur.execute("INSERT OR IGNORE INTO locations (latitude, longitude) VALUES (?, ?)", (lat, lon))
        conn.commit()

        # find location id
        cur.execute("SELECT id FROM locations WHERE latitude=? AND longitude=?", (lat, lon))
        loc_row = cur.fetchone()
        if not loc_row:
            print("  Failed to insert/find location:", lat, lon)
            continue
        loc_id = loc_row[0]

        cur.execute("SELECT 1 FROM aqi_results WHERE location_id = ?", (loc_id,))
        if cur.fetchone():
            continue

        data = fetch_aqi(lat, lon)
        if data is None:
            print(f"  Failed to fetch AQI for {lat},{lon} (API returned error). Will retry later.")
            continue

        # store raw API snapshot
        raw_json_data.append({
            "latitude": lat,
            "longitude": lon,
            "api_response": data
        })
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
            loc_id,
            d.get("aqi"),
            d.get("dominentpol"),
            d.get("time", {}).get("iso"),
            val("pm25"), val("pm10"), val("o3"), val("no2"),
            val("so2"), val("co"),
            json.dumps(data)
        ))
        conn.commit()
        added += 1
        print("  Added AQI entry for", lat, lon)

    print("\nFinished. Added:", added, "new AQI entries.")


def aqi_category(aqi):
    if aqi is None:
        return "Unknown"
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def calculate_num_category_aq():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("""
        SELECT aqi_results.aqi
        FROM aqi_results
    """)

    rows = cur.fetchall()
    #conn.close()

    summary = {}

    for (aqi,) in rows:
        category = aqi_category(aqi)

        if category not in summary:
            summary[category] = {"count": 0}
        summary[category]["count"] += 1

    return summary

# Calculation for Micah and Amy APIs

def walkscore_per_aqi():
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("""SELECT aqi.aqi, ws.description FROM aqi_results aqi
        JOIN location_mapping lm ON aqi.location_id = lm.aqi_location_id
        JOIN walkscore_results ws ON ws.location_id = lm.location_id""")
    rows = cur.fetchall()
    #conn.close()

    total_wp = {}
    walkers_paradise_counts = {}

    for aqi, description in rows:
        category1 = aqi_category(aqi)
        total_wp[category1] = total_wp.get(category1, 0) + 1
        if description == "Walkers Paradise":
            walkers_paradise_counts[category1] = walkers_paradise_counts.get(category1, 0) + 1
    rates = {}
    for category, total in total_wp.items():
        wp_count = walkers_paradise_counts.get(category, 0)
        rates[category] = wp_count / total if total > 0 else 0
    return rates

def main():
    print("Collecting AQI data (next 25 coords)...")
    get_top_cities_aqi()

    print("\nAQI Category Summary:")
    summary = calculate_num_category_aq()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()


# TEXT OUTPUT OF CALCULATIONS

traffic_list = []

cur.execute("""
SELECT current_speed, freeflow_speed
FROM DanTrafficFlow
""")
rows_traffic = cur.fetchall()
for row in rows_traffic:
    addition = row[0] + row[1]
    average = addition / 2
    #print(average)
    traffic_list.append(average)

print("THIS IS THE TRAFFIC DATA")
print(traffic_list)
print(len(traffic_list))

walkscore_list = []

cur.execute("""
SELECT walkscore, transit_score, bike_score
FROM walkscore_results
""")
rows_walkscore = cur.fetchall()
for row in rows_walkscore:
    #print('THIS IS THE ROW')
    #print(row)
    a = row[0] or 0
    b = row[1] or 0
    c = row[2] or 0
    addition = a + b + c
    if b == 0:
        average = addition / 2
    else:
        average = addition / 3
    reverse_walkscore = 100 - average
    walkscore_list.append(reverse_walkscore)

print("THIS IS THE WALKSCORE DATA")
print(walkscore_list)
print(len(walkscore_list))

counter = 0

final_coordinates_score = []

for item in traffic_list:
    try:
        average = item + walkscore_list[counter] / 2
    except:
        continue
    counter += 1
    final_coordinates_score.append(average)

cur.execute("""
SELECT latitude, longitude
FROM locations
""")

final_coordinates_dict = {}

rows_coordinates = cur.fetchall()
counter_2 = 0
for row in rows_coordinates:
    try:
        final_coordinates_dict[f"{row[0]},{row[1]}"] = final_coordinates_score[counter_2]
    except:
        continue
    counter_2 += 1

#print(final_coordinates_dict)

print("THIS IS THE FINAL DICTIONARY")
print(final_coordinates_dict)
print(len(final_coordinates_dict))

conn.commit()

with open("outputs.txt", "a") as file:
    file.write("\nOverall combined score for Walkscore and Traffic Flow. The higher the score, the more cars/car dependent the location is:\n")
    for key, value in final_coordinates_dict.items():
        file.write(f"Overall combined score for {key}: {value}\n")

def traffic_aqi_relationship():
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT aqi.aqi, tf.current_speed, tf.freeflow_speed
    FROM aqi_results aqi
    JOIN locations loc ON aqi.location_id = loc.id
    JOIN DanTrafficFlow tf ON tf.coordinates_id = loc.id
    """)

    rows = cur.fetchall()
    #conn.close()

    results = {}

    for aqi_value, current, freeflow in rows:
        category = aqi_category(aqi_value)

        congestion = max(freeflow - current, 0)
        if category not in results:
            results[category] = {"total": 0, "count": 0}

        results[category]["total"] += congestion
        results[category]["count"] += 1
    
    final = {}
    for category, info in results.items():
        avg = info["total"] / info["count"] if info["count"] > 0 else 0
        final[category] = {
            "avg_congestion": avg,
            "count": info["count"]
        }
    
    return final

traffic_vs_aqi = traffic_aqi_relationship()
print(json.dumps(traffic_vs_aqi, indent=2))

with open("outputs.txt", "a") as f:
    f.write("\n\nTraffic Congestion vs AQI Category:\n")
    for category, stats in traffic_vs_aqi.items():
        f.write(f"{category}: Average Congestion = {stats['avg_congestion']}, Count = {stats['count']}\n")

def visualize_traffic_vs_aqi(traffic_vs_aqi):
    categories = list(traffic_vs_aqi.keys())
    avg_congestion = [traffic_vs_aqi[c]["avg_congestion"] for c in categories]
    
    plt.figure(figsize=(10, 6))
    plt.bar(categories, avg_congestion)
    
    plt.xlabel("AQI Category")
    plt.ylabel("Average Traffic Congestion\n(freeflow_speed - current_speed)")
    plt.title("Average Traffic Congestion by AQI Category")
    plt.tight_layout()
    plt.savefig("traffic_vs_aqi.png")
    plt.show()
    plt.close()

print("ABOUT TO DRAW GRAPH!!!!")
visualize_traffic_vs_aqi(traffic_vs_aqi)

# DANIEL'S VISUALISATION

visualisation_dict = {}

cur.execute("""
SELECT freeflow_speed, freeflow_travel_time
FROM DanTrafficFlow
""")
rows = cur.fetchall()
for row in rows:
    visualisation_dict[row[0]] = row[1]

print(visualisation_dict)

visualisation_sorted =sorted(visualisation_dict.items(), key=lambda x: x[1])
song_name, play_count = zip(*visualisation_sorted)
fig = plt.figure(1, figsize=(10,5))
ax1 = fig.add_subplot(111)
ax1.scatter(song_name, play_count, color = "green")
ax1.ticklabel_format(axis="x", style="plain")
ax1.set_xlabel("Freeflow Speed")
ax1.set_ylabel("Freeflow Travel Time")
ax1.set_title("Scatterplot of Freeflow Speed vs Freeflow Travel Time")
plt.tight_layout()
plt.savefig("traffic_flow.png")
plt.show()
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
    "34.0522,-118.2437", # Los Angeles, CA
    "41.8781,-87.6298",  # Chicago, IL
    "29.7604,-95.3698",  # Houston, TX
    "33.4484,-112.0740", # Phoenix, AZ
    "39.9526,-75.1652",  # Philadelphia, PA
    "29.4241,-98.4936",  # San Antonio, TX
    "32.7157,-117.1611", # San Diego, CA
    "32.7767,-96.7970",  # Dallas, TX
    "37.3382,-121.8863", # San Jose, CA
    "30.2672,-97.7431",  # Austin, TX
    "30.3322,-81.6557",  # Jacksonville, FL
    "32.7555,-97.3308",  # Fort Worth, TX
    "39.9612,-82.9988",  # Columbus, OH
    "35.2271,-80.8431",  # Charlotte, NC
    "37.7749,-122.4194", # San Francisco, CA
    "39.7684,-86.1581",  # Indianapolis, IN
    "47.6062,-122.3321", # Seattle, WA
    "39.7392,-104.9903", # Denver, CO
    "38.9072,-77.0369",  # Washington, DC
    "42.3601,-71.0589",  # Boston, MA
    "31.7619,-106.4850", # El Paso, TX
    "36.1627,-86.7816",  # Nashville, TN
    "42.3314,-83.0458",  # Detroit, MI
    "35.4676,-97.5164",  # Oklahoma City, OK
    "45.5051,-122.6750", # Portland, OR
    "36.1699,-115.1398", # Las Vegas, NV
    "35.1495,-90.0490",  # Memphis, TN
    "38.2527,-85.7585",  # Louisville, KY
    "39.2904,-76.6122",  # Baltimore, MD
    "43.0389,-87.9065",  # Milwaukee, WI
    "35.0844,-106.6504", # Albuquerque, NM
    "32.2226,-110.9747", # Tucson, AZ
    "36.7378,-119.7871", # Fresno, CA
    "38.5816,-121.4944", # Sacramento, CA
    "33.4152,-111.8315", # Mesa, AZ
    "33.7490,-84.3880",  # Atlanta, GA
    "41.2565,-95.9345",  # Omaha, NE
    "38.8339,-104.8214", # Colorado Springs, CO
    "35.7796,-78.6382",  # Raleigh, NC
    "36.8529,-75.9780",  # Virginia Beach, VA
    "25.7617,-80.1918",  # Miami, FL
    "33.7701,-118.1937", # Long Beach, CA
    "37.8044,-122.2711", # Oakland, CA
    "44.9778,-93.2650",  # Minneapolis, MN
    "39.1031,-84.5120",  # Cincinnati, OH
    "43.0731,-89.4012",  # Madison, WI
    "35.0456,-85.3097",  # Chattanooga, TN
    "39.7397,-75.5390",  # Camden, NJ
    "32.6781,-83.2220",  # Augusta, GA
    "29.9511,-90.0715",  # New Orleans, LA
    "30.6954,-88.0399",  # Mobile, AL
    "40.4406,-79.9959",  # Pittsburgh, PA
    "43.6532,-79.3832",  # Toronto, ON
    "40.7357,-74.1724",  # Newark, NJ
    "42.1015,-72.5898",  # Springfield, MA
    "33.5207,-86.8025",  # Birmingham, AL
    "32.7765,-79.9311",  # Charleston, SC
    "38.6270,-90.1994",  # St. Louis, MO
    "36.0972,-79.7745",  # Greensboro, NC
    "40.7306,-73.9352",  # Queens, NY
    "41.6005,-93.6091",  # Des Moines, IA
    "36.7783,-119.4179", # Central California
    "40.6501,-73.9496",  # Brooklyn, NY
    "34.0007,-81.0348",  # Columbia, SC
    "36.7468,-119.7726", # Fresno (downtown), CA
    "48.7491,-122.4787", # Bellingham, WA
    "36.1539,-95.9928",  # Tulsa, OK
    "27.3364,-82.5307",  # Sarasota, FL
    "40.0140,-105.2705", # Boulder, CO
    "44.3148,-85.6024",  # Central Michigan
    "35.7796,-76.5500",  # Eastern North Carolina
    "32.3513,-87.0200",  # Western Alabama
    "33.8333,-116.5453", # Palm Springs, CA
    "46.8772,-96.7898",  # Fargo, ND
    "44.9537,-93.0900",  # St. Paul, MN
    "39.7686,-94.8466",  # St. Joseph, MO
    "36.1745,-86.7679",  # Nashville Metro
    "40.8258,-73.2307",  # Brentwood, NY
    "35.3733,-119.0187", # Bakersfield, CA
    "44.0805,-103.2310", # Rapid City, SD
    "43.1242,-77.6300",  # Rochester, NY
    "42.8864,-78.8784",  # Buffalo, NY
    "32.2988,-90.1848",  # Jackson, MS
    "39.5403,-119.7486", # Reno, NV
    "27.9506,-82.4572",  # Tampa, FL
    "30.4383,-84.2807",  # Tallahassee, FL
    "45.7833,-108.5007", # Billings, MT
    "41.4993,-81.6944",  # Cleveland, OH
    "33.4942,-111.9261", # Scottsdale, AZ
    "46.7296,-94.6859",  # Brainerd, MN
    "40.7673,-111.8902", # Salt Lake City, UT
    "39.1950,-106.8370", # Aspen, CO
    "48.0518,-122.1771", # Everett, WA
    "30.2241,-92.0198",  # Lafayette, LA
    "29.9511,-95.0584",  # Pasadena, TX
    "37.9470,-122.0652", # Walnut Creek, CA
    "40.7608,-111.8910", # SLC Downtown, UT
    "44.9637,-92.9594",  # Woodbury, MN
    "39.7390,-75.5640",  # Wilmington, DE
    "35.9940,-78.8986",  # Durham, NC
    "32.0835,-81.0998",  # Savannah, GA
    "37.5407,-77.4360",  # Richmond, VA
    "43.2081,-71.5376",  # Concord, NH
    "46.8770,-102.7897", # Dickinson, ND
    "35.1983,-111.6513", # Flagstaff, AZ
    "41.0938,-73.5180",  # Stamford, CT
    "32.6099,-85.4808",  # Auburn, AL
    "29.4246,-98.4951",  # San Antonio center
    "34.1808,-118.3089", # Burbank, CA
    "38.4405,-122.7144", # Santa Rosa, CA
    "37.3212,-120.4850", # Merced, CA
    "47.2529,-122.4443", # Tacoma, WA
    "33.4484,-112.0740", # Phoenix Metro
    "45.6298,-122.6733", # Vancouver, WA
    "39.6133,-105.0166", # Littleton, CO
    "40.6023,-75.4714",  # Allentown, PA
    "33.1581,-117.3506", # Carlsbad, CA
    "26.1224,-80.1373",  # Fort Lauderdale, FL
    "46.8605,-113.9960", # Missoula, MT
    "33.9533,-117.3962", # Riverside, CA
    "28.5384,-81.3789",  # Orlando, FL
    "41.6611,-91.5302",  # Iowa City, IA
    "47.6588,-117.4260", # Spokane, WA
    "40.7934,-77.8600",  # State College, PA
    "34.7465,-92.2896",  # Little Rock, AR
    "42.7325,-84.5555",  # Lansing, MI
    "38.0293,-78.4767",  # Charlottesville, VA
    "37.2047,-93.2923",  # Springfield, MO
    "27.7731,-82.6403",  # St. Petersburg, FL
    "36.1750,-115.1372", # Las Vegas Strip
    "33.5207,-86.8025",  # Birmingham Metro
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

#MAYBE REMOVE

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


#maybe remove
# cur.execute("""
# DROP TABLE IF EXISTS DanTrafficFlow
# """)
# conn.commit()


cur.execute("""
CREATE TABLE IF NOT EXISTS DanTrafficFlow (
id INTEGER PRIMARY KEY AUTOINCREMENT,
current_speed INTEGER,
freeflow_speed INTEGER,
current_travel_time INTEGER,
freeflow_travel_time INTEGER,
location_id INTEGER NOT NULL,
UNIQUE(location_id, current_travel_time),
FOREIGN KEY (location_id) REFERENCES locations(id)
)
""")
conn.commit()

counter = 0

rows_inserted = 0
maximum_rows = 25

for location in json_data:
    if rows_inserted >= maximum_rows:
        break
    current_speed = location["flowSegmentData"]["currentSpeed"]
    #print(current_speed)
    freeflow_speed = location["flowSegmentData"]["freeFlowSpeed"]
    current_travel_time = location["flowSegmentData"]["currentTravelTime"]
    freeflow_travel_time = location["flowSegmentData"]["freeFlowTravelTime"]
    latitude, longitude = coordinate_points[counter].split(",")

    cur.execute("""

    SELECT id FROM locations WHERE latitude = ? AND longitude = ?
    """, (latitude, longitude))
    location_id = cur.fetchone()

    if location_id:
        location_id = location_id[0]
    
        cur.execute("""
        INSERT OR IGNORE INTO DanTrafficFlow (current_speed, freeflow_speed, current_travel_time, freeflow_travel_time, location_id)
        VALUES (?, ?, ?, ?, ?) """, (current_speed, freeflow_speed, current_travel_time, freeflow_travel_time, location_id))
        # rows_inserted += 1
        if cur.rowcount == 1:
            rows_inserted += 1

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
    JOIN DanTrafficFlow tf ON tf.location_id = loc.id
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

with open("outputs.txt", "a") as out:
    out.write("\nTraffic Congestion × AQI Category Analysis\n")
    out.write("This section summarizes the average traffic congestion levels for each AQI category.\n")
    out.write("Congestion is calculated as: freeflow_speed - current_speed.\n\n")

    for category, stats in traffic_vs_aqi.items():
        avg_cong = stats["avg_congestion"]
        count = stats["count"]
        out.write(f"\nAQI Category: {category}\n")
        out.write(f"  • Data points: {count}\n")
        out.write(f"  • Average congestion: {avg_cong:.2f}\n")

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
freeflow_speed, freeflow_travel_time = zip(*visualisation_sorted)
fig = plt.figure(1, figsize=(10,5))
ax1 = fig.add_subplot(111)
ax1.scatter(freeflow_speed, freeflow_travel_time, color = "green")
ax1.ticklabel_format(axis="x", style="plain")
ax1.set_xlabel("Freeflow Speed")
ax1.set_ylabel("Freeflow Travel Time")
ax1.set_title("Scatterplot of Freeflow Speed vs Freeflow Travel Time")
plt.tight_layout()
plt.savefig("traffic_flow.png")
plt.show()
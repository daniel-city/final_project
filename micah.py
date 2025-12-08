import requests
import sqlite3
import time
import json
import matplotlib.pyplot as plt

api_key = "823ebf192a9537ddb2cbb92ea29ff225"

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

def get_walkscore(lat, lon):
    url = f"https://api.walkscore.com/score?format=json&lat={lat}&lon={lon}&transit=1&bike=1&wsapikey={api_key}"
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
    total = sum(count for _, count in results)
    with open("outputs.txt", "w") as f:
        f.write(f"Total locations: {total}\n\n")
        for description, count in results:
            f.write(f"{description}: {count}\n")

def main():
    conn = sqlite3.connect("test.db")
    create_SQL(conn)
    get_coords(conn, coordinate_points)
    results = num_description_and_visual(conn)
    conn.close()
    calc_and_write(results)


if __name__ == "__main__":
    main()

# def walkscore_per_aqi():
#     conn = sqlite3.connect("test.db")
#     cur = conn.cursor()
#     cur.execute("""SELECT aqi.aqi, ws.description FROM aqi_results aqi
#         JOIN location_mapping lm ON aqi.location_id = lm.aqi_location_id
#         JOIN walkscore_results ws ON ws.location_id = lm.location_id""")
#     rows = cur.fetchall()
#     conn.close()

#     total_wp = {}
#     walkers_paradise_counts = {}

#     for aqi, description in rows:
#         category1 = aqi_category(aqi)
#         total_wp[category1] = total_wp.get(category1, 0) + 1
#         if description == "Walkers Paradise":
#             walkers_paradise_counts[category1] = walkers_paradise_counts.get(category1, 0) + 1
#     rates = {}
#     for category, total in total_wp.items():
#         wp_count = walkers_paradise_counts.get(category, 0)
#         rates[category] = wp_count / total if total > 0 else 0
#     return rates

# def get_top_songs(db) -> dict:
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     cur.execute("""SELECT tracks.name AS track_name, artists.name AS artist_name, COUNT(*) AS play_count FROM listening_history
#         JOIN tracks ON listening_history.track_id = tracks.id
#         JOIN albums ON tracks.album_id = albums.id
#         JOIN artists ON albums.artist_id = artists.id
#         GROUP BY tracks.name, artists.name
#         ORDER BY play_count DESC
#         LIMIT 5;""")
#     rows = cur.fetchall()
#     conn.close()

#     top_songs = {}
#     for track, artist, play_count in rows:
#         top_songs[track] = play_count

#     plt.figure(figsize=(10, 6))
#     plt.barh(list(top_songs.keys()), list(top_songs.values()))
#     plt.xlabel("Play Count")
#     plt.title("Top 5 Most-Played Songs")
#     plt.gca().invert_yaxis()
#     plt.tight_layout()
#     plt.savefig("top_songs.png")
#     plt.close()

#     return top_songs
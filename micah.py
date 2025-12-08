import requests
import sqlite3
import time
import json
import matplotlib.pyplot as plt

api_key = "823ebf192a9537ddb2cbb92ea29ff225"

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
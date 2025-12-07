import json
import requests
import sqlite3
import os

# !!! CODE FOR API

api_key = "WZ2qAuxTYFo7cOtQYZqISrrrdj6HSpYs"
point_test = '52.41072,4.84239'
point_test_2 = '42.281735,-83.739992'
#url = "https://api.tomtom.com/map/1/tile/basic/main/0/0/0.png?view=Unified&key=YOUR_API_KEY"
#url = "https://api.tomtom.com/map/1/tile/basic/main/0/0/0.png"
#url = "https://api.tomtom.com/"
#url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={Your_API_Key}&point=52.41072,4.84239"
url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
#response = requests.get(f"{url}?view=Unified&key={api_key}")



# !!! CODE FOR COORDINATE POINTS

coordinate_points = [

'42.281735,-83.739992',
'43.281735,-83.739992',
'40.762315,-73.990162'

]

# !!! CODE FOR PUTTING DATA INTO JSON

one_hundred_data = []

for coordinate in coordinate_points:
    params = {
        'key': api_key,
        'point': coordinate,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            data["coordinates input"] = coordinate
            one_hundred_data.append(data)
            print(data)
        except requests.exceptions.JSONDecodeError:
            print("Response:", response.text)
    else:
        print(f"Error:  + {response.status_code}")

with open("traffic_flow_data.json", "w") as f:
    json.dump(one_hundred_data, f, indent=4)


# !!!CODE FOR CONVERTING JSON DATA INTO PYTHON

full_path = os.path.join(os.path.dirname(__file__), "traffic_flow_data.json")
f = open(full_path)
file_data = f.read()
f.close()
json_data = json.loads(file_data)


# !!! CODE FOR SQL

# db_name = "TrafficFlow.db"
# path = os.path.dirname(os.path.abspath(__file__))
# conn = sqlite3.connect(path + "/" + db_name)
# cur = conn.cursor()

# cur.execute("""
# DROP TABLE IF EXISTS TrafficFlow
# """)

# cur.execute("""
# CREATE TABLE IF NOT EXISTS TrafficFlow (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# current_speed INTEGER,
# freeflow_speed INTEGER,
# current_travel_time INTEGER,
# freeflow_travel_time INTEGER,
# latitude FLOAT,
# longitude FLOAT
# )
# """)
# counter = 0

# for location in json_data:
#     current_speed = location["flowSegmentData"]["currentSpeed"]
#     #print(current_speed)
#     freeflow_speed = location["flowSegmentData"]["freeFlowSpeed"]
#     current_travel_time = location["flowSegmentData"]["currentTravelTime"]
#     freeflow_travel_time = location["flowSegmentData"]["freeFlowTravelTime"]
#     latitude = coordinate_points[counter][:9]
#     longitude = coordinate_points[counter][10:]
#     counter += 1
#     cur.execute("""
#     INSERT OR IGNORE INTO TrafficFlow (current_speed, freeflow_speed, current_travel_time, freeflow_travel_time, latitude, longitude)
#     VALUES (?, ?, ?, ?, ?, ?) """, (current_speed, freeflow_speed, current_travel_time, freeflow_travel_time, latitude, longitude))

# # conn.commit()

# # for coordinate in coordinate_points:
# #     latitude = coordinate[:9]
# #     longitude = coordinate[10:]
# #     cur.execute("""
# #     INSERT OR IGNORE INTO TrafficFlow (latitude, longitude)
# #     VALUES (?, ?) """, (latitude, longitude))

# conn.commit()
# conn.close()



db_name = "test.db"
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + db_name)
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS test
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS test (
id INTEGER PRIMARY KEY AUTOINCREMENT,
current_speed INTEGER,
freeflow_speed INTEGER,
current_travel_time INTEGER,
freeflow_travel_time INTEGER,
latitude FLOAT,
longitude FLOAT
)
""")
counter = 0

for location in json_data:
    current_speed = location["flowSegmentData"]["currentSpeed"]
    #print(current_speed)
    freeflow_speed = location["flowSegmentData"]["freeFlowSpeed"]
    current_travel_time = location["flowSegmentData"]["currentTravelTime"]
    freeflow_travel_time = location["flowSegmentData"]["freeFlowTravelTime"]
    latitude = coordinate_points[counter][:9]
    longitude = coordinate_points[counter][10:]
    counter += 1
    cur.execute("""
    INSERT OR IGNORE INTO test (current_speed, freeflow_speed, current_travel_time, freeflow_travel_time, latitude, longitude)
    VALUES (?, ?, ?, ?, ?, ?) """, (current_speed, freeflow_speed, current_travel_time, freeflow_travel_time, latitude, longitude))

# conn.commit()

# for coordinate in coordinate_points:
#     latitude = coordinate[:9]
#     longitude = coordinate[10:]
#     cur.execute("""
#     INSERT OR IGNORE INTO TrafficFlow (latitude, longitude)
#     VALUES (?, ?) """, (latitude, longitude))

conn.commit()
conn.close()
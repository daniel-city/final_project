import json
import requests
import sqlite3
import os


api_key = "WZ2qAuxTYFo7cOtQYZqISrrrdj6HSpYs"
point_test = '52.41072,4.84239'
point = '42.281735,-83.739992'
#url = "https://api.tomtom.com/map/1/tile/basic/main/0/0/0.png?view=Unified&key=YOUR_API_KEY"
#url = "https://api.tomtom.com/map/1/tile/basic/main/0/0/0.png"
#url = "https://api.tomtom.com/"
#url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={Your_API_Key}&point=52.41072,4.84239"
url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
#response = requests.get(f"{url}?view=Unified&key={api_key}")

coordinate_points = [

'42.281735,-83.739992',
'43.281735,-83.739992',
'44.281735,-83.739992'

]

one_hundred_data = []

for coordinate in coordinate_points:
    params = {
        'key': api_key,
        'point': point,
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


# full_path = os.path.join(os.path.dirname(__file__), "traffic_flow_data.json")
# f = open(full_path)
# file_data = f.read()
# f.close()
# json_data = json.loads(file_data)

db_name = "test_database_dan"
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + "/" + db_name)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS TrafficFlow (
current_speed INTEGER PRIMARY KEY,
freeflow_speed INTEGER,
current_travel_time INTEGER,
freeflow_travel_time INTEGER,
latitude FLOAT,
longitude FLOAT
)
""")
import json
import requests
import sqlite3

api_key = "WZ2qAuxTYFo7cOtQYZqISrrrdj6HSpYs"
point_test = '52.41072,4.84239'
point = '42.281735,-83.739992'
#url = "https://api.tomtom.com/map/1/tile/basic/main/0/0/0.png?view=Unified&key=YOUR_API_KEY"
#url = "https://api.tomtom.com/map/1/tile/basic/main/0/0/0.png"
#url = "https://api.tomtom.com/"
#url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={Your_API_Key}&point=52.41072,4.84239"
url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
#response = requests.get(f"{url}?view=Unified&key={api_key}")

params = {
    'key': api_key,
    'point': point,
}
response = requests.get(url, params=params)

if response.status_code == 200:
    try:
        data = response.json()
        print(data)
    except requests.exceptions.JSONDecodeError:
        print("Response:", response.text)
else:
    print(f"Error:  + {response.status_code}")

with open("traffic_flow_data.json", "w") as f:
    json.dump(data, f, indent=4)
    
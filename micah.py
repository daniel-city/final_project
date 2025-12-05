import requests
import json

api_key = "823ebf192a9537ddb2cbb92ea29ff225"
lat = input("Enter latitude: ").strip()
lon = input("Enter longitude: ").strip()

try:
    lat = float(lat)
    lon = float(lon)
except ValueError:
    print("Invalid latitude or longitude. Please enter numeric values.")
    exit()

url = f"https://api.walkscore.com/score?format=json&lat={lat}&lon={lon}&transit=1&bike=1&wsapikey={api_key}"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("status") != 1:
        print(f"API returned an error: {data.get('status')}, {data.get('error')}")
    else:
        with open("walkscore_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
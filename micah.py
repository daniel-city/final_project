import requests
import json

api_key = "823ebf192a9537ddb2cbb92ea29ff225"
url = f"https://api.walkscore.com/score?format=json&lat=47.6085&lon=-122.3295&transit=1&bike=1&wsapikey={api_key}"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    with open("walkscore_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Data saved successfully.")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# def get_walkscore_full(lat, lon, api_key, include_transit=True, include_bike=True):
#     url = "https://api.walkscore.com/score"

#     params = {
#         "format": "json",
#         "lat": lat,
#         "lon": lon,
#         "transit": 1 if include_transit else 0,
#         "bike": 1 if include_bike else 0,
#         "wsapikey": api_key
#     }

#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()

#         if data.get("status") != 1:
#             return {"error": "Walk Score API returned an error", "status": data.get("status")}

#         return {
#             "walk": {
#                 "score": data.get("walkscore"),
#                 "description": data.get("description")
#             },
#             "transit": {
#                 "score": data.get("transit", {}).get("score"),
#                 "description": data.get("transit", {}).get("description")
#             } if include_transit else None,
#             "bike": {
#                 "score": data.get("bike", {}).get("score"),
#                 "description": data.get("bike", {}).get("description")
#             } if include_bike else None
#         }

#     except Exception as e:
#         return {"error": str(e)}

import json
import sqlite3
import os
import requests

API_KEY = "bd1842990d39e66f7830f18d756cb443636008b7"

top_cities_file = "top100_cities.json"
raw_json_file = "aqi_data.json"
db_file = "air_quality.db"

batch_size = 25
import json
import sqlite3
import os
import requests

API_KEY = "bd1842990d39e66f7830f18d756cb443636008b7"

top_cities_file = "top100_cities.json"
raw_json_file = "aqi_data.json"
db_file = "air_quality.db"

batch_size = 25

def load_top_cities():
    if not os.path.exists(top_cities_file):
        raise FileNotFoundError(f"{top_cities_file} not found.")
    with open(top_cities_file, "r") as f:
        return json.load(f)
    

def init_db():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    #cities table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        country TEXT,
        lat REAL,
        lon REAL
    )
    """)

    #AQI readings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS AQIReadings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER,
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
            FOREIGN KEY(city_id) REFERENCES Cities(id)
        )
    """)

    conn.commit()
    return conn, cur
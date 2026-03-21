# -*- coding: utf-8 -*-
"""
Flask backend - read/write weather_data.json
"""

from flask import Flask, request, jsonify, send_from_directory
import json
import os

# Disable default static-file route (prevents /static/server.py exposure)
app = Flask(__name__, static_folder=None)

DATA_FILE = 'weather_data.json'
MAX_FAVORITES = 50
MAX_STRING_LEN = 100

# ── Security headers ───────────────────────────────────────────────────────────
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://unpkg.com; "
        "style-src 'self' 'unsafe-inline' https://unpkg.com https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; "
        "img-src 'self' data: https://*.tile.openstreetmap.org https://unpkg.com; "
        "connect-src 'self' https://api.open-meteo.com https://geocoding-api.open-meteo.com;"
    )
    return response

# ── Input validation ──────────────────────────────────────────────────────────
def validate_city(city):
    """Return (ok, error_message). Accepts only safe city objects."""
    if not isinstance(city, dict):
        return False, 'Invalid payload'
    name = city.get('name')
    country = city.get('country', '')
    lat = city.get('lat')
    lon = city.get('lon')
    if not isinstance(name, str) or not name.strip():
        return False, 'Missing or invalid name'
    if not isinstance(country, str):
        return False, 'Invalid country'
    if len(name) > MAX_STRING_LEN or len(country) > MAX_STRING_LEN:
        return False, 'Name or country too long'
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return False, 'lat/lon must be numbers'
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        return False, 'lat/lon out of range'
    return True, None

# ── Data helpers ──────────────────────────────────────────────────────────────
def init_data_file():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "favoriteCities": [],
            "defaultCapitals": [
                {"name": "Beijing", "country": "China", "lat": 39.9042, "lon": 116.4074},
                {"name": "Tokyo", "country": "Japan", "lat": 35.6762, "lon": 139.6503},
                {"name": "Seoul", "country": "South Korea", "lat": 37.5665, "lon": 126.978},
                {"name": "London", "country": "United Kingdom", "lat": 51.5074, "lon": -0.1278},
                {"name": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
                {"name": "New York", "country": "United States", "lat": 40.7128, "lon": -74.006},
                {"name": "Sydney", "country": "Australia", "lat": -33.8688, "lon": 151.2093},
                {"name": "Moscow", "country": "Russia", "lat": 55.7558, "lon": 37.6173},
                {"name": "Berlin", "country": "Germany", "lat": 52.52, "lon": 13.405},
                {"name": "Singapore", "country": "Singapore", "lat": 1.3521, "lon": 103.8198},
                {"name": "Dubai", "country": "UAE", "lat": 25.2048, "lon": 55.2708},
                {"name": "Mumbai", "country": "India", "lat": 19.076, "lon": 72.8777},
                {"name": "Bangkok", "country": "Thailand", "lat": 13.7563, "lon": 100.5018},
                {"name": "Cairo", "country": "Egypt", "lat": 30.0444, "lon": 31.2357},
                {"name": "Rome", "country": "Italy", "lat": 41.9028, "lon": 12.4964}
            ]
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)

def read_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading data: {e}")
        return {"favoriteCities": [], "defaultCapitals": []}

def write_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error writing data: {e}")
        return False

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(read_data())

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    data = read_data()
    return jsonify(data.get('favoriteCities', []))

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    city = request.get_json(silent=True)
    ok, err = validate_city(city)
    if not ok:
        return jsonify({"success": False, "error": err}), 400

    # Sanitise: keep only the fields we need
    clean = {
        "name":    city['name'].strip(),
        "country": city.get('country', '').strip(),
        "lat":     float(city['lat']),
        "lon":     float(city['lon']),
    }

    data = read_data()
    favorites = data.get('favoriteCities', [])

    if len(favorites) >= MAX_FAVORITES:
        return jsonify({"success": False, "error": "Favorites list is full"}), 400

    if not any(f.get('name') == clean['name'] for f in favorites):
        favorites.append(clean)
        data['favoriteCities'] = favorites
        write_data(data)

    return jsonify({"success": True, "favorites": favorites})

@app.route('/api/favorites/<city_name>', methods=['DELETE'])
def remove_favorite(city_name):
    if len(city_name) > MAX_STRING_LEN:
        return jsonify({"success": False, "error": "Invalid city name"}), 400
    data = read_data()
    favorites = data.get('favoriteCities', [])
    favorites = [f for f in favorites if f.get('name') != city_name]
    data['favoriteCities'] = favorites
    write_data(data)
    return jsonify({"success": True, "favorites": favorites})

if __name__ == '__main__':
    init_data_file()
    print("Server running at http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)

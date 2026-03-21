# -*- coding: utf-8 -*-
"""
简单的 Flask 后端 - 用于读写 weather_data.json
"""

from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__, static_folder='.')

DATA_FILE = 'weather_data.json'

# 初始化数据文件
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

# 读取数据
def read_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading data: {e}")
        return {"favoriteCities": [], "defaultCapitals": []}

# 写入数据
def write_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error writing data: {e}")
        return False

# 主页
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 获取所有数据
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(read_data())

# 获取关注城市列表
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    data = read_data()
    return jsonify(data.get('favoriteCities', []))

# 添加关注城市
@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    data = read_data()
    city = request.json
    
    # 检查是否已存在
    favorites = data.get('favoriteCities', [])
    if not any(f.get('name') == city.get('name') for f in favorites):
        favorites.append(city)
        data['favoriteCities'] = favorites
        write_data(data)
    
    return jsonify({"success": True, "favorites": favorites})

# 删除关注城市
@app.route('/api/favorites/<city_name>', methods=['DELETE'])
def remove_favorite(city_name):
    data = read_data()
    favorites = data.get('favoriteCities', [])
    favorites = [f for f in favorites if f.get('name') != city_name]
    data['favoriteCities'] = favorites
    write_data(data)
    
    return jsonify({"success": True, "favorites": favorites})

if __name__ == '__main__':
    init_data_file()
    print("Server running at http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)

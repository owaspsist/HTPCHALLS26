from flask import Flask, request, jsonify, send_from_directory
import os
import math

app = Flask(__name__, static_folder='static')

# --- CHALLENGE CONFIGURATION ---
TARGET_LAT = 1.404639   # 1°24'16.7"N
TARGET_LNG = 103.795528 # 103°47'43.9"E
THRESHOLD_KM = 0.010    # 10-meter buffer

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/guess', methods=['POST'])
def guess():
    data = request.json
    if not data or 'lat' not in data or 'lng' not in data:
        return jsonify({"error": "Invalid coordinates"}), 400

    user_lat = float(data['lat'])
    user_lng = float(data['lng'])

    distance = haversine(user_lat, user_lng, TARGET_LAT, TARGET_LNG)

    if distance <= THRESHOLD_KM:
        flag = os.environ.get('GZCTF_FLAG', 'Flag not set in environment.')
        return jsonify({"success": True, "flag": flag})
    else:
        return jsonify({"success": False, "message": "Incorrect location. Target missed."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9995)

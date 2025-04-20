from flask import Flask, jsonify, request, g
from flask_cors import CORS
import json
import os
import time

app = Flask(__name__)
CORS(app)


# 📌 Middleware
@app.before_request
def middleware():
    g.start_time = time.time()

    if request.path == '/api/packages' and request.method == 'GET':
        # Ensure packages.json exists
        if not os.path.exists('packages.json'):
            print("⚠️ packages.json not found. Creating one...")
            with open('packages.json', 'w') as f:
                json.dump([], f, indent=2)

        # Log request to log.json
        log_action("GET /api/packages", {"ip": request.remote_addr})
        packages = []
        
        g.packages = [p for p in packages if p.get('price', 0) >= 0]
        print(f"📦 Loaded {len(g.packages)} packages.")


# 📌 Logging Function
def log_action(action, details):
    log_entry = {
        "action": action,
        "details": details,
        "ip": request.remote_addr,
        "time": time.strftime('%Y-%m-%d %H:%M:%S')
    }

    log_path = 'log.json'
    if not os.path.exists(log_path):
        with open(log_path, 'w') as f:
            json.dump([], f, indent=2)

    with open(log_path, 'r+') as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, indent=2)


# 📌 Main API Route
@app.route('/api/packages', methods=['GET'])
def get_packages():
    with open('packages.json') as f:
        packages = json.load(f)
    return jsonify(packages)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

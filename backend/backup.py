from flask import Flask, jsonify, request, g
from flask_cors import CORS
import json
import os
import time

app = Flask(__name__)
CORS(app)

def log_action(action, details):
    log_entry = {
        "action": action,
        "details": details,
        "ip": request.remote_addr,
        "time": time.strftime('%Y-%m-%d %H:%M:%S')
    }

    if not os.path.exists('log.json'):
        with open('log.json', 'w') as f:
            json.dump([], f)

    with open('log.json', 'r+') as f:
        logs = json.load(f)
        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, indent=2)

@app.before_request
def middleware():
    g.start_time = time.time()

    print(f"📥 Request: {request.method} {request.path} from {request.remote_addr}")

    if request.path == '/api/packages' and request.method == 'GET':
        if not os.path.exists('packages.json'):
            print("⚠️ packages.json not found. Creating a new one...")
            with open('packages.json', 'w') as f:
                json.dump([], f, indent=2)  # empty list

        try:
            with open('packages.json') as f:
                packages = json.load(f)
        except json.JSONDecodeError:
            print("❌ Invalid JSON format. Resetting packages.json...")
            with open('packages.json', 'w') as f:
                json.dump([], f, indent=2)
            packages = []

        # You can also modify or log here
        g.packages = [p for p in packages if p.get('price', 0) >= 0]
        print(f"📦 Loaded {len(g.packages)} packages.")


@app.after_request
def after_middleware(response):
    duration = time.time() - g.get('start_time', time.time())
    print(f"🕒 Completed in {duration:.3f}s")
    return response


# === Route ===
@app.route('/api/packages', methods=['GET'])
def get_packages():
    # Use preloaded packages from middleware
    return jsonify(g.get('packages', []))


if __name__ == '__main__':
    app.run(debug=True, port=5000)

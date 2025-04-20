from flask import Flask, jsonify, request, g
from flask_cors import CORS
import json
import os
import time

app = Flask(__name__)
CORS(app)

# === LOGGING FUNCTION ===
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
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, indent=2)


# === MIDDLEWARE BEFORE REQUEST ===
@app.before_request
def middleware():
    g.start_time = time.time()
    print(f"📥 Request: {request.method} {request.path} from {request.remote_addr}")

    # Log every request
    log_action(f"{request.method} {request.path}", {
        "method": request.method,
        "headers": dict(request.headers),
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "json": request.get_json(silent=True)
    })

    # Specific behavior for GET /api/packages
    if request.path == '/api/packages' and request.method == 'GET':
        if not os.path.exists('packages.json'):
            print("⚠️ packages.json not found. Creating a new one...")
            with open('packages.json', 'w') as f:
                json.dump([], f, indent=2)

        try:
            with open('packages.json') as f:
                packages = json.load(f)
        except json.JSONDecodeError:
            print("❌ Invalid JSON format. Resetting packages.json...")
            with open('packages.json', 'w') as f:
                json.dump([], f, indent=2)
            packages = []

        # Optional validation/modification
        g.packages = [p for p in packages if p.get('price', 0) >= 0]
        print(f"📦 Loaded {len(g.packages)} packages.")


# === MIDDLEWARE AFTER REQUEST ===
@app.after_request
def after_middleware(response):
    duration = time.time() - g.get('start_time', time.time())
    print(f"🕒 Completed in {duration:.3f}s")
    return response


# === GET PACKAGES ROUTE ===
@app.route('/api/packages', methods=['GET'])
def get_packages():
    return jsonify(g.get('packages', []))


# === ADMIN ACTION (EXAMPLE POST) ===
@app.route('/api/packages', methods=['POST'])
def add_package():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON'}), 400

    new_package = {
        "destination": data.get('destination'),
        "price": data.get('price'),
        "duration": data.get('duration')
    }

    if not all(new_package.values()):
        return jsonify({'error': 'Missing fields in request'}), 400

    # Load or create package list
    if not os.path.exists('packages.json'):
        with open('packages.json', 'w') as f:
            json.dump([], f, indent=2)

    with open('packages.json', 'r+') as f:
        try:
            packages = json.load(f)
        except json.JSONDecodeError:
            packages = []

        packages.append(new_package)
        f.seek(0)
        json.dump(packages, f, indent=2)

    print(f"✅ Admin added new package: {new_package}")
    log_action("ADD PACKAGE", new_package)
    return jsonify({"message": "Package added successfully."}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)

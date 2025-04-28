from flask import Flask, jsonify, request, g
from flask_cors import CORS
import json
import os
import time
import getpass 


app = Flask(__name__)
CORS(app)

PACKAGES_FILE = 'packages.json'
LOG_FILE = 'log.json'

def log_action(action, details):
    log_entry = {
        "action": action,
        "details": details,
        "ip": request.remote_addr,
        "time": time.strftime('%Y-%m-%d %H:%M:%S')
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)

    with open(LOG_FILE, 'r+') as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, indent=2)



def ensure_package_file():
    if not os.path.exists(PACKAGES_FILE):
        print("⚠️ packages.json not found. Creating a new one...")
        with open(PACKAGES_FILE, 'w') as f:
            json.dump([], f, indent=2)


def load_packages():
    ensure_package_file()
    try:
        with open(PACKAGES_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("❌ Invalid JSON format. Resetting packages.json...")
        with open(PACKAGES_FILE, 'w') as f:
            json.dump([], f, indent=2)
        return []


def save_packages(packages):
    with open(PACKAGES_FILE, 'w') as f:
        json.dump(packages, f, indent=2)



@app.before_request
def middleware():
    g.start_time = time.time()

    user_agent = request.headers.get('User-Agent', '').lower()
    is_browser = 'mozilla' in user_agent or 'chrome' in user_agent or 'safari' in user_agent
    is_admin = not is_browser

    request_type = "🌐 CLIENT" if is_browser else "🛠️ ADMIN"
    print(f"{request_type} | {request.method} {request.path} from {request.remote_addr}")
    print(f"🛡️ User-Agent: {user_agent}")
    print(f"🛡️ Is Browser: {is_browser}")
    g.user_agent = user_agent
    g.is_browser = is_browser
    g.is_admin = is_admin
    g.start_time = time.time()
    g.packages = []
    
    if is_browser:
        log_action("CLIENT_REQUEST", {
            "path": request.path,
            "method": request.method,
            "user_agent": request.headers.get('User-Agent'),
            "query": request.args.to_dict()
        })


    if request.path == '/api/packages' and request.method == 'GET':
        packages = load_packages()
        g.packages = [p for p in packages if p.get('price', 0) >= 0]
        print(f"📦 Loaded {len(g.packages)} packages.")


@app.after_request
def after_middleware(response):
    duration = time.time() - g.get('start_time', time.time())
    print(f"🕒 Completed in {duration:.3f}s")
    return response



@app.route('/api/packages', methods=['GET'])
def get_packages():
    return jsonify(g.get('packages', []))


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
        return jsonify({'error': 'Missing fields'}), 400

    packages = load_packages()
    packages.append(new_package)
    save_packages(packages)

    print(f"✅ Admin added: {new_package}")
    log_action("ADD PACKAGE", new_package)
    return jsonify({"message": "Package added"}), 201


@app.route('/api/packages/<int:index>', methods=['PUT'])
def update_package(index):
    data = request.get_json()
    packages = load_packages()

    if index < 0 or index >= len(packages):
        return jsonify({'error': 'Package index out of range'}), 404

    updated_package = packages[index]
    updated_package.update({
        "destination": data.get('destination', updated_package.get('destination')),
        "price": data.get('price', updated_package.get('price')),
        "duration": data.get('duration', updated_package.get('duration')),
    })

    packages[index] = updated_package
    save_packages(packages)

    print(f"✏️ Admin updated index {index}: {updated_package}")
    log_action("UPDATE PACKAGE", {"index": index, "updated": updated_package})
    return jsonify({"message": "Package updated"})


@app.route('/api/packages/<int:index>', methods=['DELETE'])
def delete_package(index):
    packages = load_packages()

    if index < 0 or index >= len(packages):
        return jsonify({'error': 'Package index out of range'}), 404

    deleted = packages.pop(index)
    save_packages(packages)

    print(f"🗑️ Admin deleted index {index}: {deleted}")
    log_action("DELETE PACKAGE", {"index": index, "deleted": deleted})
    return jsonify({"message": "Package deleted"})


def verify_password():
    try:
        with open('auth.json') as f:
            auth = json.load(f)
            correct_pass = auth.get("admin_password")
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ auth.json not found or invalid.")
        return False

    attempt = getpass.getpass("🔐 Enter admin password to start the server: ").strip()
    return attempt == correct_pass


if __name__ == '__main__':
    if verify_password():
        print("✅ Access granted. Server starting...")
        app.run(debug=True, port=5000)
    else:
        print("🚫 Access denied. Exiting...")


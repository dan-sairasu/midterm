import json

# --- Load Admin Credentials ---
def load_admins():
    with open("admins.json") as f:
        return json.load(f)

# --- Admin Login ---
def admin_login():
    print("🛡️ Admin Login")
    username = input("Username: ")
    password = input("Password: ")
    
    admins = load_admins()
    for admin in admins:
        if admin["username"] == username and admin["password"] == password:
            print("✅ Login successful.")
            return True

    print("❌ Invalid credentials.")
    return False

# --- Load & Save Packages ---
def load_packages():
    with open('../backend/packages.json') as f:
        return json.load(f)

def save_packages(packages):
    with open('../backend/packages.json', 'w') as f:
        json.dump(packages, f, indent=2)

# --- Admin Actions ---
def add_package():
    packages = load_packages()
    destination = input("Destination: ")
    price = int(input("Price: "))
    duration = input("Duration (e.g. 5 days): ")
    new_id = max(p["id"] for p in packages) + 1 if packages else 1
    packages.append({
        "id": new_id,
        "destination": destination,
        "price": price,
        "duration": duration
    })
    save_packages(packages)
    print("✅ Package added.")

def list_packages():
    packages = load_packages()
    print("\n📦 Available Packages:")
    for p in packages:
        print(f"{p['id']}: {p['destination']} - ${p['price']} - {p['duration']}")

def delete_package():
    packages = load_packages()
    id_to_delete = int(input("Enter package ID to delete: "))
    filtered = [p for p in packages if p["id"] != id_to_delete]
    if len(filtered) == len(packages):
        print("⚠️ No package found with that ID.")
    else:
        save_packages(filtered)
        print("🗑️ Package deleted.")

# --- Admin Menu ---
def admin_menu():
    while True:
        print("\n🧭 Admin Menu")
        print("1.📃 List Packages")
        print("2.➕ Add Package")
        print("3.🗑️ Delete Package")
        print("4.🚪 Exit")
        choice = input("✅ Choice: ")
        if choice == "1":
            list_packages()
        elif choice == "2":
            add_package()
        elif choice == "3":
            delete_package()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")

# --- Main Entry Point ---
if __name__ == "__main__":
    if admin_login():
        admin_menu()

def format_report(packages):
    return "\n".join([f"{p['destination']}: ${p['price']} - {p['duration']}" for p in packages])

if __name__ == "__main__":
    import json
    with open('../backend/packages.json') as f:
        packages = json.load(f)
    print(format_report(packages))

import json
import os

HISTORY_FILE = "ip_history.json"

def load_ip_history():
    """Returns list of previously used IP addresses from JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
            return data.get("ips", [])
    except Exception:
        return []  # corrupted or unreadable file

def save_ip_history(new_ip):
    """Adds new IP to history if not already exists."""
    ips = load_ip_history()
    if new_ip not in ips:
        ips.append(new_ip)
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump({"ips": ips}, f, indent=4)
        except Exception as e:
            print("Failed to save IP history:", e)

import json
import os
from datetime import datetime

DB_FILE = "uniterm_db.json"

def load_database():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_entry(title, author, sa, sb, pa, pb, replace_first):
    db = load_database()
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    entry = {
        "title": title,
        "author": author,
        "datetime": now,
        "sa": sa,
        "sb": sb,
        "pa": pa,
        "pb": pb,
        "replace_first": replace_first
    }

    db.append(entry)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def get_all_authors():
    db = load_database()
    return sorted(set(entry["author"] for entry in db if entry["author"]))

def get_all_entries():
    return load_database()
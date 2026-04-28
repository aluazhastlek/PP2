import json
import os
from datetime import datetime

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "green",
    "difficulty": "normal"
}


def load_json(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except Exception:
            return default
    return default


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS.copy())
leaderboard = load_json(LEADERBOARD_FILE, [])
def load_settings():
    return settings


def save_settings():
    save_json(SETTINGS_FILE, settings)


def add_score(name, score, distance, coins):
    leaderboard.append({
        "name": name,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    leaderboard.sort(key=lambda item: item["score"], reverse=True)
    del leaderboard[10:]
    save_json(LEADERBOARD_FILE, leaderboard)

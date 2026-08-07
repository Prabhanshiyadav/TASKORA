import json
import os
from task import Task

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return [Task.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError):
        return []

def save_data(tasks):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    data = [task.to_dict() for task in tasks]
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
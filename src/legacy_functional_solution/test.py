import os, sys
from pathlib import Path
import json


def add_coffee(name, price):
    print(f"Adding coffee {name} at price {price}")
    return name, price


add_coffee("Ethiopian", 15.5)


# Example JSON string (array of objects)
json_str = """
[
    {"id": 1, "name": "Coffee A"},
    {"id": 2, "name": "Coffee B"},
    {"id": 3, "name": "Coffee C"}
]
"""
BASE = Path(__file__).parent
file_path = BASE / "data3.json"
print("file_path", file_path)
try:
    with open(file_path) as f:
        content = f.read()
        json_dict_data = json.loads(content)
        # print("json_dict_data", type(json_dict_data), json_dict_data["products"])
        num_objects = len(json_dict_data["products"])
        print("Number of objects:", num_objects)
except (FileNotFoundError, json.JSONDecodeError):
    print("error")

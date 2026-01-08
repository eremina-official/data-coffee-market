import requests
import json
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment variables

ACCESS_TOKEN = os.getenv("ALLEGRO_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise RuntimeError("ALLEGRO_ACCESS_TOKEN not set")


API_URL = "https://api.allegro.pl/sale/products?phrase=kawa%20palarnia"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/vnd.allegro.public.v1+json",
}

SAVE_DIR = "allegro_responses"
os.makedirs(SAVE_DIR, exist_ok=True)

params = {"limit": 100}

response = requests.get(API_URL, headers=HEADERS, params=params)

if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit(1)

data = response.json()

# Extract nextPage.id (if exists)
next_page_id = data.get("nextPage", {}).get("id", "no_next_page")
safe_cursor = urllib.parse.quote(next_page_id, safe="")

filename = f"page_1__cursor_{safe_cursor}.json"
filepath = os.path.join(SAVE_DIR, filename)

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved {filepath}")
print(f"Products in page: {len(data.get('products', []))}")
print(f"Next page cursor: {next_page_id}")

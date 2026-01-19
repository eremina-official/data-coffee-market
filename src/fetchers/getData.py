import requests
import time
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

next_page_id = None
page = 1

while True:
    if next_page_id:
        params["page.id"] = next_page_id

    response = requests.get(API_URL, headers=HEADERS, params=params)

    if response.status_code == 429:
        time.sleep(10)
        continue

    if response.status_code != 200:
        print(response.status_code, response.text)
        break

    data = response.json()

    # Create filename-safe cursor
    # cursor = next_page_id or "first_page"
    # safe_cursor = urllib.parse.quote(cursor, safe="")

    # FULL final URL (with query params resolved)
    full_url = response.url
    # Make URL filename-safe
    safe_url = urllib.parse.quote(full_url, safe="")

    filename = f"page_{page}__url_{safe_url}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved {filename}")

    products = data.get("products", [])

    if not products:
        break

    next_page = data.get("nextPage")

    if not next_page or "id" not in next_page:
        break

    next_page_id = next_page["id"]
    page += 1

    time.sleep(0.6)

print("Done")

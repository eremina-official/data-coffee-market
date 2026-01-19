import requests
import time
import json
import os
import urllib.parse
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

load_dotenv()  # loads .env into environment variables

ACCESS_TOKEN = os.getenv("ALLEGRO_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise RuntimeError("ALLEGRO_ACCESS_TOKEN not set")

api_phrase = "republika%20kawy"
API_URL = f"https://api.allegro.pl/sale/products?phrase={api_phrase}"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/vnd.allegro.public.v1+json",
}

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parents[1]

RAW_DATA_DIR = ROOT_DIR / "allegro_responses"
BATCH_NAME = f"batch_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}"
BATCH_NAME_DIR = RAW_DATA_DIR / BATCH_NAME

RAW_DATA_DIR.mkdir(exist_ok=True)  # create base folder
BATCH_NAME_DIR.mkdir(parents=True, exist_ok=True)  # create batch folder
print(ROOT_DIR)
readme_file = RAW_DATA_DIR / "README.md"

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
    filepath = BATCH_NAME_DIR / filename

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


# Prepare batch metadata
metadata = {
    "batch_name": BATCH_NAME,
    "collected_at": datetime.now().isoformat(),
    "products_count": page,
    "folder": BATCH_NAME_DIR,
}

# Append metadata to README.md
with open(readme_file, "a", encoding="utf-8") as f:
    f.write(f"## {metadata['batch_name']}\n")
    f.write(f"- Collected at: {metadata['collected_at']}\n")
    f.write(f"- API phrase: {api_phrase}\n")
    f.write(f"- API URL: {API_URL}\n")
    f.write(f"- Pages count: {metadata['products_count']}\n")
    f.write(f"- Folder: {metadata['folder']}\n\n")

print("Done")

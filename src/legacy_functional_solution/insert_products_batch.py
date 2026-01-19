import json
from insert_product import insert_product
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path_to_data = BASE_DIR.parents[1] / "allegro_responses"
folder = Path(path_to_data)
files = [f.name for f in folder.iterdir() if f.is_file()]

# print("base dir", files)

# Add data to database
for file in folder.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for product in data["products"]:
        try:
            insert_product(product)
            print(f"Inserted product: {product.get('name')}")
        except Exception as e:
            print(f"Failed to insert product {product.get('id')}: {e}")

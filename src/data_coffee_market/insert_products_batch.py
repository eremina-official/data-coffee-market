import os
import json
from insert_product import insert_product

BASE_DIR = os.path.dirname(__file__)
# Go up two levels to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
# Path to your JSON file
file_path = os.path.join(
    PROJECT_ROOT,
    "allegro_responses",
    "page_1__url_https%3A%2F%2Fapi.allegro.pl%2Fsale%2Fproducts%3Fphrase%3Dkawa%2520palarnia%26limit%3D100.json",
)

print(file_path)

# Load your JSON file
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# If your file contains a list of products
for product in data["products"]:
    try:
        # insert_product(product)
        print(f"Inserted product: {product.get('name')}")
    except Exception as e:
        print(f"Failed to insert product {product.get('id')}: {e}")

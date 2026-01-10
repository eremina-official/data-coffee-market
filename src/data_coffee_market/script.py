from typing import List, Dict
from models.product import Product
from db.db_connection import get_cursor
from db.insert_product import (
    insert_product,
    insert_parameter,
    insert_parameter_value,
    map_product_parameter,
)
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
path_to_data = BASE_DIR.parents[1] / "allegro_responses"
folder = Path(path_to_data)
files = [f.name for f in folder.iterdir() if f.is_file()]
file = BASE_DIR / "example.json"


def run_products_pipeline(raw_products):
    coffee_category_ids = ("74035", "74033")
    print("raw")

    for raw in raw_products:
        if raw.get("category", {}).get("id") not in coffee_category_ids:
            continue

        product = Product(**raw)
        product.ean = product.extract_ean()

        # cursor, conn = get_cursor()  # open one connection per product
        # try:
        #     # Insert parameters and values
        #     for param in product.parameters:
        #         if not getattr(param, "valuesIds", None):
        #             continue
        #         insert_parameter(param.dict(), cursor)
        #         values_labels = getattr(param, "valuesLabels", []) or []
        #         values_values = getattr(param, "values", values_labels) or []
        #         if not values_values:
        #             values_values = [None] * len(values_labels)
        #         values_ids = (
        #             getattr(
        #                 param,
        #                 "valuesIds",
        #                 [f"{param.id}_{i}" for i in range(len(values_labels))],
        #             )
        #             or []
        #         )

        #         for vid, label, val in zip(values_ids, values_labels, values_values):
        #             insert_parameter_value(
        #                 {"id": vid, "parameter_id": param.id, "value": val}, cursor
        #             )
        #             map_product_parameter(product.id, vid, cursor)

        #     # Insert product
        #     insert_product(product, cursor)

        #     conn.commit()  # commit once per product
        # finally:
        #     cursor.close()
        #     conn.close()


with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)

run_products_pipeline(data["products"])

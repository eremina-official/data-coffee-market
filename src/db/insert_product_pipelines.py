from typing import List, Dict
from models.product import Product
from db.db_connection import get_cursor
from db.insert_product_helpers import (
    insert_product,
    insert_parameter,
    insert_parameter_value,
    map_product_parameter,
)
import json
from pathlib import Path
from utils.constants import VALUES_LABELS, VALUES_IDS

BASE_DIR = Path(__file__).resolve().parent
path_to_data = BASE_DIR.parents[1] / "allegro_responses"
folder = Path(path_to_data)
files = [f.name for f in folder.iterdir() if f.is_file()]
file = BASE_DIR / "example.json"


def run_products_pipeline(raw_products, cursor):
    coffee_category_ids = ("74035", "74033")
    print("raw")

    for raw in raw_products:
        if raw.get("category", {}).get("id") not in coffee_category_ids:
            continue

        product = Product(**raw).to_db_dict()

        # Insert parameters and values
        for param in product.get("parameters", []):
            if "valuesIds" not in param:
                continue
            # print("param", type(param))
            # insert_parameter(param.dict(), cursor)

            values_labels = param.get(VALUES_LABELS, []) or []
            values_values = param.get("values", values_labels) or []

            if not values_values:
                values_values = [None] * len(values_labels)  # Fill with None for zip

            values_ids = (
                param.get(
                    VALUES_IDS,
                    [f'{param["id"]}_{i}' for i in range(len(values_labels))],
                )
                or []
            )

            for vid, label, val in zip(values_ids, values_labels, values_values):
                insert_parameter_value(
                    param_id=param["id"],
                    value_id=vid,
                    label=label,
                    value=val,
                    cursor=cursor,
                )
                map_product_parameter(
                    product_id=product.id, value_id=vid, cursor=cursor
                )

        # # Insert product
        insert_product(product, cursor)
        print(f"Inserted product: {product.get('parameters')}")


with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)

run_products_pipeline(data["products"], {})

# def main():
#     cursor, conn = get_cursor()  # Open connection once for all files
#     try:
#         for file in files:
#             with open(file, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#             run_products_pipeline(data.get("products", []), cursor)
#         conn.commit()  # commit once after all products
#     except Exception as e:
#         print(f"Error during database operation: {e}")
#     finally:
#         cursor.close()
#         conn.close()


# if __name__ == "__main__":
#     main()

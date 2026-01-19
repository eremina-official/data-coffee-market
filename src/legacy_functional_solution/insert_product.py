import json
import os
from db.db_connection import get_connection


BASE_DIR = os.path.dirname(__file__)  # folder of current script
file_path = os.path.join(BASE_DIR, "product5.json")


# === Database connection ===
conn = get_connection()
cursor = conn.cursor()


# === Helper functions ===
def insert_category(category):
    """Insert category and its parent recursively."""
    parent_id = category.get("parent_id")
    cursor.execute(
        "INSERT IGNORE INTO categories (id, name, parent_id) VALUES (%s, %s, %s)",
        (category["id"], category["name"], parent_id),
    )


def insert_parameter(param):
    """Insert parameter only if it does not exist."""
    cursor.execute(
        "INSERT IGNORE INTO parameters (id, name, unit, identifies_product) VALUES (%s, %s, %s, %s)",
        (
            param["id"],
            param["name"],
            param.get("unit"),
            param.get("options", {}).get("identifiesProduct", False),
        ),
    )


def insert_parameter_value(param_id, value_id, label, value=None):
    """Insert parameter value only if it does not exist."""
    cursor.execute(
        "INSERT IGNORE INTO parameter_values (id, parameter_id, label, value) VALUES (%s, %s, %s, %s)",
        (value_id, param_id, label, value),
    )


def map_product_parameter(product_id, value_id):
    """Map product to parameter value."""
    cursor.execute(
        "INSERT IGNORE INTO product_parameter_values (product_id, value_id) VALUES (%s, %s)",
        (product_id, value_id),
    )


# === Insert product ===
def insert_product(product):
    # Insert only 'kawa ziarnista' and 'kawa mielona' products (category ids: '74035', '74033')
    coffee_category_ids = ("74035", "74033")
    if product["category"]["id"] not in coffee_category_ids:
        return

    # Insert category and parent categories
    for cat in product["category"]["path"]:
        parent_id = cat.get("parent_id")
        cursor.execute(
            "INSERT IGNORE INTO categories (id, name, parent_id) VALUES (%s, %s, %s)",
            (cat["id"], cat["name"], parent_id),
        )

    # --- Extract EAN (GTIN) ---
    ean = None
    for param in product.get("parameters", []):
        if param["name"] == "EAN (GTIN)":
            ean = param.get("values", [param.get("valuesLabels", [None])[0]])[0]

    # Insert product
    cursor.execute(
        """
        INSERT INTO products (id, name, publication_status, description, images, category_id, ean)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE id=id
        """,
        (
            product["id"],
            product["name"],
            product.get("publication", {}).get("status"),
            json.dumps(product.get("description", {})),  # store description as JSON
            json.dumps(
                [img["url"] for img in product.get("images", [])]
            ),  # store images as JSON
            product["category"]["id"],
            ean,
        ),
    )

    # Insert parameters and parameter values
    for param in product.get("parameters", []):
        # Skip parameters without 'valuesIds' (unique id for each existing value, params like "Waga")
        if "valuesIds" not in param:
            continue

        insert_parameter(param)
        values_labels = param.get("valuesLabels", []) or []
        values_values = param.get("values", values_labels) or []

        if not values_values:
            values_values = [None] * len(values_labels)  # Fill with None for zip

        values_ids = (
            param.get(
                "valuesIds", [f'{param["id"]}_{i}' for i in range(len(values_labels))]
            )
            or []
        )
        for vid, label, val in zip(values_ids, values_labels, values_values):
            insert_parameter_value(param["id"], vid, label, val)
            map_product_parameter(product["id"], vid)

    # Commit after each product
    conn.commit()


# # if __name__ == "__main__":
# #     with open(file_path, "r", encoding="utf-8") as f:
# #         product_data = json.load(f)

# #     insert_product(product_data)
# #     cursor.close()
# #     conn.close()

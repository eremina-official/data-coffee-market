import mysql.connector
import json
import os
from db_connection import get_connection

BASE_DIR = os.path.dirname(__file__)  # folder of current script
file_path = os.path.join(BASE_DIR, "product.json")

print("get_connection", get_connection)

# Example: load product JSON from file
with open(file_path, "r", encoding="utf-8") as f:
    product = json.load(f)


def insert_product(product):
    conn = get_connection()
    cursor = conn.cursor()

    # ---- 1️⃣ Insert product ----
    description_text = ""
    for section in product.get("description", {}).get("sections", []):
        for item in section.get("items", []):
            if item.get("type") == "TEXT":
                description_text += item.get("content", "") + "\n"

    cursor.execute(
        """
        INSERT INTO products (id, name, publication_status, description)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), publication_status=VALUES(publication_status), description=VALUES(description)
    """,
        (
            product["id"],
            product["name"],
            product.get("publication", {}).get("status"),
            description_text.strip(),
        ),
    )

    # ---- 2️⃣ Insert categories ----
    def insert_category_path(path):
        parent_id = None
        for cat in path:
            cursor.execute(
                """
                INSERT INTO categories (id, name, parent_id)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), parent_id=VALUES(parent_id)
            """,
                (cat["id"], cat["name"], parent_id),
            )
            parent_id = cat["id"]

    insert_category_path(product["category"]["path"])

    # ---- 3️⃣ Map product to main category ----
    main_cat_id = product["category"]["id"]
    cursor.execute(
        """
        INSERT IGNORE INTO product_categories (product_id, category_id)
        VALUES (%s, %s)
    """,
        (product["id"], main_cat_id),
    )

    # ---- 4️⃣ Insert parameters ----
    for param in product.get("parameters", []):
        cursor.execute(
            """
            INSERT INTO parameters (id, name, unit, identifies_product)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name=VALUES(name), unit=VALUES(unit), identifies_product=VALUES(identifies_product)
        """,
            (
                param["id"],
                param["name"],
                param.get("unit"),
                param.get("options", {}).get("identifiesProduct", False),
            ),
        )

        # ---- 5️⃣ Insert parameter values ----
        for idx, label in enumerate(param.get("valuesLabels", [])):
            value_id = None
            if param.get("valuesIds"):
                value_id = param["valuesIds"][idx]
            value_val = None
            if param.get("values"):
                value_val = param["values"][idx]
            cursor.execute(
                """
                INSERT INTO parameter_values (id, parameter_id, label, value)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE label=VALUES(label), value=VALUES(value)
            """,
                (value_id, param["id"], label, value_val),
            )

            # ---- 6️⃣ Map product to parameter value ----
            if value_id:
                cursor.execute(
                    """
                    INSERT IGNORE INTO product_parameter_values (product_id, value_id)
                    VALUES (%s, %s)
                """,
                    (product["id"], value_id),
                )

    # ---- 7️⃣ Insert images ----
    for img in product.get("images", []):
        cursor.execute(
            """
            INSERT IGNORE INTO images (url)
            VALUES (%s)
        """,
            (img["url"],),
        )
        cursor.execute(
            """
            INSERT IGNORE INTO product_images (product_id, image_id)
            SELECT %s, id FROM images WHERE url = %s
        """,
            (product["id"], img["url"]),
        )

    # Commit all changes
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted product {product['name']} ({product['id']}) successfully!")


# if __name__ == "__main__":
#     insert_product(product)

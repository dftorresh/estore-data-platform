import random

from database import Database
from datetime import datetime
from simulator.catalog import PRODUCT_CATALOG

def create_sku(category, brand, model):
    category_code = category[:3].upper()
    brand_code = brand[:3].upper()
    model_code = "".join(
        c for c in model.upper()
        if c.isalnum()
    )[:6]
    return f"{category_code}-{brand_code}-{model_code}"


PRICE_RANGES = {
    "Laptops": (700, 2500),
    "Monitors": (150, 900),
    "Accessories": (20, 250),
    "Gaming": (70, 700),
    "Networking": (50, 600),
    "Storage": (40, 500),
    "Kitchen": (80, 900),
    "Smart Home": (40, 400),
    "Audio": (30, 500)
}


def seed_products(db):

    current_datetime =  datetime.utcnow()

    categories = db.fetch_all(
        """
        SELECT
            category_id,
            category_name
        FROM Categories
        WHERE
            category_name != 'Office'
        """
    )

    suppliers = db.fetch_all(
        """
        SELECT supplier_id
        FROM Suppliers
        """
    )

    supplier_ids = [s["supplier_id"] for s in suppliers]

    for category in categories:

        category_name = category["category_name"]

        for brand, model in PRODUCT_CATALOG[category_name]:

            db.execute(
                """
                INSERT INTO Products
                (
                    category_id,
                    supplier_id,
                    product_name,
                    sku,
                    unit_price,
                    created_at,
                    updated_at
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s,%s
                )
                """,
                (
                    category["category_id"],
                    random.choice(supplier_ids),
                    f"{brand} {model}",
                    create_sku(category_name, brand, model),
                    round(
                        random.uniform(
                            *PRICE_RANGES[category_name]
                        ),
                        2
                    ),
                    current_datetime,
                    current_datetime
                )
            )


def seed_inventory(db):

    warehouses = db.fetch_all(
        """
        SELECT warehouse_id
        FROM Warehouses
        """
    )

    products = db.fetch_all(
        """
        SELECT product_id
        FROM Products
        """
    )

    for warehouse in warehouses:

        for product in products:

            db.execute(
                """
                INSERT INTO Inventory
                (
                    warehouse_id,
                    product_id,
                    quantity_available
                )
                VALUES
                (
                    %s,%s,%s
                )
                """,
                (
                    warehouse["warehouse_id"],
                    product["product_id"],
                    random.randint(20, 250)
                )
            )
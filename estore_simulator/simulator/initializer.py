from database import Database
from simulator.product_simulator import (
    seed_inventory,
    seed_products
)

CATEGORIES = [
    "Laptops",
    "Monitors",
    "Accessories",
    "Gaming",
    "Networking",
    "Storage",
    # "Office",
    "Kitchen",
    "Smart Home",
    "Audio"
]

SUPPLIERS = [
    ("Contoso Electronics", "sales@contoso.com", "USA"),
    ("Northwind Components", "sales@northwind.com", "Canada"),
    ("Fabrikam Devices", "sales@fabrikam.com", "Germany"),
    ("Adventure Works", "sales@adventureworks.com", "USA"),
    ("Tailspin Toys", "sales@tailspin.com", "Japan")
]

WAREHOUSES = [
    ("Miami Warehouse", "Miami", "USA"),
    ("Dallas Warehouse", "Dallas", "USA"),
    ("Toronto Warehouse", "Toronto", "Canada")
]


def initialize():

    with Database() as db:

        total = db.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM Categories
            """
        )["total"]

        if total > 0:

            print("Database already initialized.")

            return

        print("Creating Categories...")

        db.executemany(
            """
            INSERT INTO Categories(category_name)
            VALUES(%s)
            """,
            [(category,) for category in CATEGORIES]
        )

        print("Creating Suppliers...")

        db.executemany(
            """
            INSERT INTO Suppliers
            (
                supplier_name,
                contact_email,
                country
            )
            VALUES(%s,%s,%s)
            """,
            SUPPLIERS
        )

        print("Creating Warehouses...")

        db.executemany(
            """
            INSERT INTO Warehouses
            (
                warehouse_name,
                city,
                country
            )
            VALUES(%s,%s,%s)
            """,
            WAREHOUSES
        )

        print("Creating Products...")

        seed_products(db)

        print("Creating Inventory...")

        seed_inventory(db)

        print("Initialization completed.")
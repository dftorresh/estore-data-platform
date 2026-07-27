from database import execute, fetch_one
from simulator.product_simulator import (
    seed_products,
    seed_inventory
)

CATEGORIES = [
    "Laptops",
    "Monitors",
    "Accessories",
    "Gaming",
    "Networking",
    "Storage",
    #"Office",
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

    count = fetch_one(
        "SELECT COUNT(*) AS total FROM Categories"
    )["total"]

    if count > 0:
        print("Database already initialized.")
        return

    print("Creating Categories...")

    for category in CATEGORIES:

        execute(
            """
            INSERT INTO Categories(category_name)
            VALUES(%s)
            """,
            (category,)
        )

    print("Creating Suppliers...")

    for supplier in SUPPLIERS:

        execute(
            """
            INSERT INTO Suppliers
            (
                supplier_name,
                contact_email,
                country
            )
            VALUES(%s,%s,%s)
            """,
            supplier
        )

    print("Creating Warehouses...")

    for warehouse in WAREHOUSES:

        execute(
            """
            INSERT INTO Warehouses
            (
                warehouse_name,
                city,
                country
            )
            VALUES(%s,%s,%s)
            """,
            warehouse
        )

    print("Creating Products...")
    seed_products()

    print("Creating Inventory...")
    seed_inventory()

    print("Initialization completed.")
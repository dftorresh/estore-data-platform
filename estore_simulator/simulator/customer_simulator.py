import random
from faker import Faker
from config_simulation import SIMULATION
from database import Database

fake = Faker()


def register_customers(db: Database):

    total = random.randint(
        *SIMULATION["new_customers_per_day"]
    )

    print(f"\nRegistering {total} new customers...\n")

    for _ in range(total):
        register_customer(db)

    print(f"{total} customers registered.\n")


def register_customer(db: Database):

    customer = (
        fake.first_name(),
        fake.last_name(),
        fake.unique.email(),
        fake.phone_number()
    )

    db.execute(
        """
        INSERT INTO Customers
        (
            first_name,
            last_name,
            email,
            phone
        )
        OUTPUT INSERTED.customer_id
        VALUES
        (
            %s,%s,%s,%s
        )
        """,
        customer
    )

    customer_id = db.cursor.fetchone()["customer_id"]
    create_addresses(db, customer_id)


def create_addresses(db: Database, customer_id: int):

    billing = (
        customer_id,
        "Billing",
        fake.street_address(),
        None,
        fake.city(),
        fake.state(),
        fake.country(),
        fake.postcode()
    )

    shipping = (
        customer_id,
        "Shipping",
        fake.street_address(),
        None,
        fake.city(),
        fake.state(),
        fake.country(),
        fake.postcode()
    )

    db.executemany(
        """
        INSERT INTO Addresses
        (
            customer_id,
            address_type,
            address_line1,
            address_line2,
            city,
            state,
            country,
            postal_code
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s
        )
        """,
        [billing, shipping]
    )